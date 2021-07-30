from setuptools import setup

long_desc = open("README.md").read() + "\n\n" + open("HISTORY.md").read()
required = ['requests']

setup(
    name='PyCalendly',
    version="0.0.1",
    maintainer="laxmena",
    maintainer_email="ConnectWith@laxmena.com",
    license="MIT",
    url="https://github.com/laxmena/PyCalendly",
    download_url="https://github.com/laxmena/PyCalendly",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    version='1.0.0',
    description="Python wrapper for Calendly API v2 (https://calendly.stoplight.io/docs/api-docs/docs/C-API-Conventions.md)",
    include_package_data=True,
    zip_safe=False,
    install_requires=required,
    platforms="any",
    keywords="Calendly python api v2",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python"
    ]
)