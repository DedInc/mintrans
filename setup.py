from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mintrans",
    version="1.0.1",
    author="Maehdakvan",
    author_email="visitanimation@google.com",
    description="Mintrans is a free API wrapper that utilizes Bing Translator for translation purposes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DedInc/mintrans",
    project_urls={
        "Bug Tracker": "https://github.com/DedInc/mintrans/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=['requests'],
    python_requires='>=3.6'
)
