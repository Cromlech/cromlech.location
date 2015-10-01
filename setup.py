from setuptools import setup, find_packages
import os


version = '1.0+crom'

install_requires = [
    'crom',
    'cromlech.browser >= 0.5',
    'setuptools',
    'zope.interface',
    'zope.location',
    ]

tests_require = [
    'cromlech.browser [test]',
    'pytest',
    'zope.testing',
    ]

setup(name='cromlech.location',
      version=version,
      description="URL computing using locatability (``zope.location``)",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Cromlech Location',
      author='The Cromlech team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org/',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['cromlech',],
      include_package_data=True,
      zip_safe=False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
