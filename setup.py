from setuptools import setup, find_packages

setup(
    name='argv',
    version='0.0.2',
    description='Simpler command line argument parsing',
    url='https://github.com/chbrown/argv',
    author='Christopher Brown',
    author_email='io@henrian.com',
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    packages=find_packages(),
    # https://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
