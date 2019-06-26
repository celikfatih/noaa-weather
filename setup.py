import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="noaa-weather",
    version="0.1",
    scripts=["noaa/get_historical_weather.py"],
    author="Fatih Celik",
    author_email="fatih.celik@b2metric.com",
    description="A bulk historical weather data from National Oceanic and Atmospheric Administration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/celikfatih",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)