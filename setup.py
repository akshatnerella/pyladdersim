from setuptools import setup, find_packages

setup(
    name='pyladdersim',
    version='0.1.1',
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        'matplotlib',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.10',
    description='A Python-based ladder logic simulation library with visualization tools',
    author='Akshat Nerella',
    author_email='akshatnerella27@gmail.com',
    url='https://github.com/akshatnerella/pyladdersim',
)
