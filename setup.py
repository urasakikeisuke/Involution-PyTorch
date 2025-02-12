import os
from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from torch.utils.cpp_extension import CppExtension, CUDAExtension, BuildExtension

INCLUDE_DIR = join(dirname(abspath(__file__)), 'include')
EXTRA_COMPILE_ARGS = ['-O3']

EXTENSION = []

CC = ['52', '53', '60', '61', '62', '70', '72', '75', '80']

if os.getenv('USE_OPENMP', '1') == '1':
    EXTRA_COMPILE_ARGS.append('-fopenmp')

if os.getenv('USE_CUDA', '1') == '1':
    EXTRA_COMPILE_ARGS.append('-DUSE_CUDA')

    GENERATE_CODES = []

    for cc in CC:
        GENERATE_CODES.append('--generate-code')
        GENERATE_CODES.append(f'arch=compute_{cc},code=compute_{cc}')

    EXTENSION.append(
        CUDAExtension(
            name='involution',
            sources=[
                'src/involution2d_cpu.cpp',
                'src/involution2d_cuda.cu',
                'src/pytorch_wrapper.cpp',
            ],
            include_dirs=[
                INCLUDE_DIR
            ],
            extra_compile_args={
                'cxx': EXTRA_COMPILE_ARGS,
                'nvcc': ['-O3'] + GENERATE_CODES,
            }
        )
    )
else:
    EXTENSION.append(
        CppExtension(
            name='involution',
            sources=[
                'src/involution2d_cpu.cpp',
                'src/pytorch_wrapper.cpp',
            ],
            include_dirs=[
                INCLUDE_DIR
            ],
            extra_compile_args=EXTRA_COMPILE_ARGS
        )
    )

setup(
    name='involution-pytorch',
    version="0.2.2",
    url="https://github.com/shikishima-TasakiLab/Involution-PyTorch",
    license="MIT License",
    author="Junya Shikishima",
    author_email="160442065@ccalumni.meijo-u.ac.jp",
    description="PyTorch Involution",
    packages=find_packages(),
    ext_modules=EXTENSION,
    cmdclass={
        'build_ext': BuildExtension,
    }
)
