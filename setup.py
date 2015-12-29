import setuptools

setuptools.setup(
    name = "mockserver-client",
    version = "0.0.1",
    packages = setuptools.find_packages(),
    author='Job Evers-Meltzer',
    author_email='jobevers@gmail.com',
    url='https://github.com/jobevers/mockserver-client-python',
    description='A client for http://www.mock-server.com/',
    long_description=open('README.md').read(),
    install_requires=[
        'requests'
    ],
)
