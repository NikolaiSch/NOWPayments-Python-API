"""
Setup
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nowpay",
    version="2.1.0",
    author="@NikolaiSch",
    author_email="NikolaiS@tuta.io",
    description="NOWPayments python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NikolaiSch/NowPay-Python",
    project_urls={
        "Bug Tracker": "https://github.com/NikolaiSch/NowPay-Python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
