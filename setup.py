import io

from setuptools import setup

setup(
    name='botoinator',
    version='0.0.1',
    description='A decoration mechanism for boto3 that allows automatic decoration of any and all boto3 clients and resources',
    author='Joseph Wortmann',
    author_email='jwortmann@quinovas.com',
    url='https://github.com/QuiNovas/apigatewaydisconnectapi',
    license='Apache 2.0',
    long_description=io.open('README.md', encoding='utf-8').read(),
    packages=['botoinator'],
    package_dir={'botoinator': 'src/botoinator'},
    install_requires = [],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
)
