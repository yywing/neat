import pkg_resources
import setuptools

with open('requirements.txt', "r") as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neat-client-python",
    version="0.0.1",
    author="yywing",
    author_email="386542536@qq.com",
    description="Neat client for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yywing/neat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=install_requires,
)
