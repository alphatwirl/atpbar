from setuptools import setup, find_packages
import versioneer

long_description = """
atpbar
------

Progress bars for threading and multiprocessing tasks on terminal and
Jupyter Notebook.

The code in *atpbar* started its development in 2015 as part of
`alphatwirl <https://github.com/alphatwirl/alphatwirl>`__. It has been a
sub-package, *progressbar*, of alphatwirl. It became an independent
package in February 2019. *atpbar* can display multiple progress bars
simultaneously growing to show the progresses of iterations of loops
in `threading <https://docs.python.org/3/library/threading.html>`__ or
`multiprocessing <https://docs.python.org/3/library/multiprocessing.html>`__
tasks. *atpbar* can display progress bars on terminal and `Jupyter
Notebook <https://jupyter.org/>`__.

- How to use atpbar is explained at https://github.com/alphatwirl/atpbar.
"""

setup(
    name='atpbar',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Progress bars for threading and multiprocessing tasks',
    long_description=long_description,
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
