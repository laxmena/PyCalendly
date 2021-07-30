from setuptools import setup

long_desc = open("README.md").read() + "\n\n" + open("HISTORY.md").read()
required = []

setup(
    name='PyCalendly',
    maintainer="laxmena",
    maintainer_email="ConnectWith@laxmena.com",
    license="MIT",
    url="https://github.com/laxmena/PyCalendly",
    download_url="https://github.com/laxmena/PyCalendly",
    long_description=long_desc,
    version='1.0.0',
    description="Python wrapper for Calendly API v2 (https://calendly.stoplight.io/docs/api-docs/docs/C-API-Conventions.md)",
    include_package_data=True,
    zip_safe=False,
    install_requires=required,
    platforms="any",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python"
    ]
)