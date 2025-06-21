from setuptools import setup

setup(
    name="ttoolly-utils",
    version="0.1.1",
    description="useful tools for test development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Polina Mishchenko",
    author_email="polina.v.mishchenko@gmail.com",
    url="https://github.com/pefremova/ttoolly-utils",
    license_files=("LICENSE.txt",),
    packages=[
        "ttoolly_utils",
    ],
    python_requires=">=3.10",
    extras_require={"images": ["Pillow>=11.2"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
)
