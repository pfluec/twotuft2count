from setuptools import setup, find_packages

setup(
    name='twotuft2count',
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
        'instanseg-torch',
        'fcswrite',
        'scikit-image'
    ],
    entry_points={
        'console_scripts': [
            'cellquant=cellquant.cli:main',
        ],
    },
)
