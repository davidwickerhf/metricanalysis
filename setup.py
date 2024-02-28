from setuptools import setup, find_packages

setup(
    name='metrics',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add your project dependencies here
        'click',
        'pandas',
        'numpy',
        'matplotlib',
        'networkx',
        'networkit',
    ],
    entry_points={
        'console_scripts': [
            'metrics=metrics.cli.metrics:cli',
        ],
    },
    author='David Henry Francis Wicker',
    author_email='david.wicker@maastrichtuniversity.nl',
    description='Tool to streamline testing and analysis of node centrality metrics',
    url='https://github.com/davidwickerhf/metricanalysis',
)