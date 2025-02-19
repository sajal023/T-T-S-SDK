from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:  # ✅ Explicit UTF-8 encoding
    long_description = fh.read()

setup(
    name="tts_sdk",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "numpy",
        "soundfile",
        "langdetect",
        "langid",
    ],
    author="Sajal Srivastav",
    description="Multilingual Text-to-Speech SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tts_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
