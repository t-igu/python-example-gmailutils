import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gmailutils", # Replace with your own username
    version="0.1.0",
    # entry_points={
    #     'console_scripts': [
    #         'corona=corona:main',
    #     ],
    # },
    author="me",

    # author_email="me@example.com",
    description="Get message and send mail from Gmail.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/me/sampleproject",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "requests", 
        "google-api-python-client",
        "google-auth",
        "requests-oauthlib",
        "google_auth_oauthlib",
        "html2text",
        "pytz",
        "python-dateutil",
    ],
    python_requires='>=3.7',
)