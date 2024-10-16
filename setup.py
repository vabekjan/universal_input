from setuptools import setup, find_packages

setup(
    name='universal_input',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'h5py',  # Specify version or just the package name
        'numpy'  
    ],
    entry_points={
        'console_scripts': [
            'create_universal_HDF5=create_universal_HDF5:run',  # The command `my_script` calls the script directly
        ],
    },
)