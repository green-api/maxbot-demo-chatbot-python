from setuptools import setup, find_packages

setup(
    name="maxbot-demo-chatbot-python",
    version="1.0.1",
    description="Python demo chatbot for MAX bot",
    author="Green-API",
    url="https://github.com/green-api/maxbot-demo-chatbot-python",
    packages=find_packages(),
    install_requires=[
        "maxbot-api-client-python",
        "maxbot-chatbot-python",
        "httpx",
        "python-dotenv",
        "PyYAML",
        "pydantic"
    ],
    python_requires=">=3.8",
)