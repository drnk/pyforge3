from setuptools import setup

setup(
    name="compound-data-tool",
    version="0.1",
    py_modules=["cdt"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        cdt=src.cdt:cli
    """,
)
