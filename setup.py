from setuptools import setup

setup(
    name="C_Geek's Blog",
    packages=['blog'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)