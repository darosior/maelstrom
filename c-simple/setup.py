import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as r:
    requirements = [line[:-1] for line in r]

setuptools.setup(
    name='c-simple',
    version='0.0.4',
    license='MIT',
    author='Antoine Poinsot',
    author_email='darosior@protonmail.com',
    description='The API for c-simple, a Lightning Network wallet',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Bitcoin, Lighning network, c-simple, csimple, bitcoin',
    url='https://github.com/darosior/c-simple',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=requirements
)
