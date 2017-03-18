from setuptools import setup

setup(
    name="libutils",
    version="0.1.0",
    description="Reusable, generic utility package",
    long_description="Utility Library.",
    keywords="utilities",
    author="James Tarball <james.tarball@gmail.com>",
    author_email="james.tarball@gmail.com",
    url="https://github.com/javaab/libutils",
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
