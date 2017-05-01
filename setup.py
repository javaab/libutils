from setuptools import setup

from libutils import __version__


setup(
    name="libutils",
    version=__version__,
    description="Reusable, generic utility package",
    long_description="Utility Library.",
    keywords="utilities",
    author="James Tarball <james.tarball@newtonsystems.co.uk>",
    author_email="james.tarball@newtonsystems.co.uk",
    url="https://github.com/newtonsystems/libutils",
    license="MIT license",
    packages=["libutils"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
