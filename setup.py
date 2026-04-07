from setuptools import setup, find_packages

with open("README.md", encoding="UTF-8") as file:
    long_description = file.read()

setup(
    name="maxbot-demo-chatbot-python",
    version="1.1.0",
    description="Python demo chatbot for MAX bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Green-API",
    url="https://github.com/green-api/maxbot-demo-chatbot-python",
    packages=find_packages(),
    install_requires=[
        "maxbot-api-client-python>=1.1.2",
        "maxbot-chatbot-python>=1.1.0",
        "httpx>=0.28.1",
        "python-dotenv>=1.0.1",
        "PyYAML>=6.0.2",
        "pydantic>=2.10.6"
    ],
    python_requires=">=3.12",
)