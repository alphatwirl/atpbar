from setuptools import setup, find_packages
import versioneer

from pathlib import Path

here = Path(__file__).resolve().parent
long_description = here.joinpath('README.md').read_text()

setup(
    name='atpbar',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Progress bars for threading and multiprocessing tasks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tai Sakuma',
    author_email='tai.sakuma@gmail.com',
    url='https://github.com/alphatwirl/atpbar',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    extras_require={
        'tests': [
            'pytest>=5.4',
            'pytest-cov>=2.8',
            'pytest-console-scripts>=0.2',
            # 'mantichora>=0.10',
        ],
        'jupyter': [
            'jupyter>-1.0',
            'ipywidgets>=7.5',
        ]
    }
)
