from setuptools import setup, find_packages

setup(
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    include_package_data=True,
    install_requires=["jinja2==3.1.2", "pyyaml==5.4.1", "jsonschema==4.7.2"],
    entry_points={
        "console_scripts": ["openassetio-traitgen=openassetio_traitgen.__main__:main"],
    },
)
