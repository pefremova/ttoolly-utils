from setuptools import setup

setup(
    name="ttoolly-utils",
    version="0.1",
    description="useful tools for test development",
    author="Polina Mishchenko",
    author_email="polina.v.mishchenko@gmail.com",
    packages=[
        "ttoolly_utils",
    ],
    python_requires=">=3.10",
    extras_require={"images": ["Pillow>=11.2"]},
)
