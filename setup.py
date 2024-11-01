from setuptools import setup, find_packages

setup(
    name='ladder_sim',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Education, Learning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    description='A Python-based ladder logic simulation library with visualization tools',
    author='Akshat Nerella',
    author_email='akshatnerella27@gmail.com'
)
