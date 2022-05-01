import setuptools

setuptools.setup(
    name="TikTokPrinter",
    packages=setuptools.find_packages(),
    version="0.0.6",
    license="MIT",
    description="TikTokLive Printer Library",
    author="Isaac Kogan",
    author_email="info@isaackogan.com",
    url="https://github.com/isaackogan/TikTokPrinter",
    long_description_content_type="text/markdown",
    keywords=["tiktok", "tiktok live", "python3", "api", "unofficial"],
    install_requires=[
        "aiohttp>=3.8",  # Make requests
        "protobuf3-to-dict>=0.1.5",  # Convert Protobuf to Dict
        "protobuf>=3.19.4",  # Decode Protobuf Messages
        "pyee>=9.0.4",  # Event Emitter
        "dacite>=1.6.0",  # Requests
        "TikTokLive",
        "pyttsx3",
        "playsound==1.2.2",
        "python-escpos==2.2.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Framework :: aiohttp",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)
