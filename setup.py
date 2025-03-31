from setuptools import setup, find_packages

setup(
    name="questionarie",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "": ["static/*", "data/*"],
    },
    install_requires=[
        "streamlit",
        "sqlalchemy",
        "psycopg2-binary",
        "pandas",
        "python-dotenv",
    ],
)
