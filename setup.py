from setuptools import setup, find_packages

setup(
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    include_package_data=True,
    # We are currently constrained to pyyaml=6.0.0 exactly due to conan 1.60.1
    install_requires=["jinja2==3.1.2", "pyyaml==6.0.0", "jsonschema==4.7.2"],
    entry_points={
        "console_scripts": ["openassetio-traitgen=openassetio_traitgen.__main__:main"],
    },
)
