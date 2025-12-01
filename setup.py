from setuptools import setup, find_packages

setup(
    name="secapi",
    version="0.1.0",
    description="A Python API wrapper to fetch SEC data and map financial statements using AI embeddings.",
    author="YOUR NAME",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.3,<3.0",
        "numpy>=2.3,<3.0",
        "requests>=2.32,<3.0",
        "sentence-transformers>=5.1,<6.0",
    ],
    python_requires=">=3.10",
)
