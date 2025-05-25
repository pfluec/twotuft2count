from setuptools import setup, find_packages

setup(
    name='2tuft2count',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'tifffile',
        'scipy',
        'napari[all]',
        'magicgui',
        'click',
        'tifftools',
        'instanseg-torch'
    ],
    entry_points={
        'console_scripts': [
            'cellquant=cellquant.cli:main',
        ],
    },
)
