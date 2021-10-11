from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='rss_reader',
    version='1.5.0',
    author='Aleksey Mikhalkevich',
    author_email='lehado67@gmail.com',
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aleksey-Mikh/Homework/tree/final_task",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
    ],
    entry_points={
        "console_scripts": [
            "rss_reader = cool_project.rss_reader:main",
        ],
    }
)