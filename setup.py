from setuptools import setup

setup(
    name="Blog",
    packages=['blog'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    entry_points={
        'flask.commands': [
            'shell=blog.tools.shell:shell_command'
        ]
    }
)
