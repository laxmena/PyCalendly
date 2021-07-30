try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_desc = open("README.md").read()
required = ['requests']

setup(
    name='PyCalendly',
    version="0.0.1",
    author="laxmena",
    author_email="ConnectWith@laxmena.com",
    license="MIT",
    url="https://github.com/laxmena/PyCalendly",
    download_url="https://github.com/laxmena/PyCalendly",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    description="Python wrapper for Calendly API v2 (https://calendly.stoplight.io/docs/api-docs/docs/C-API-Conventions.md)",
    packages=[
        'calendly',
        'calendly.utils'
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=required,
    platforms="any",
    keywords="Calendly python api v2",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python"
    ],
    python_requires=">3.6",
)