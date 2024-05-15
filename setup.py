from setuptools import setup, find_packages

setup(
    name='graph_analysis_tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'networkx',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'jupyter'
    ],
    entry_points={
        'console_scripts': [
            'graph_analysis_tool=src.main:main',
        ],
    },
    author='David Henry Francis Wicker',
    author_email='david.wicker@maastrichtuniversity.nl',
    description='A tool for analyzing legal citation networks',
    url='https://github.com/davidwickerhf/metrics',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
