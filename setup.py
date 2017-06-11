from setuptools import setup, find_packages

setup(
    name='sqltomongo',
    version='0.1',
    author='A. Mishchenko',
    author_email='a.voskresenskyi@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pymongo==3.4.0',
        'pql==0.4.3'
    ],
    entry_points='''
        [console_scripts]
        sqltomongo=sqltomongo.main:main
    ''',
)

