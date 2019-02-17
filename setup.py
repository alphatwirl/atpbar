from setuptools import setup, find_packages
import versioneer

setup(
    name='atpbar',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Progress bars for threading and multiprocessing tasks',
    author='Tai Sakuma',
    author_email='tai.sakuma@gmail.com',
    url='https://github.com/alphatwirl/atpbar',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['docs', 'tests'])
)
