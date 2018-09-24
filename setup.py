import os.path
import setuptools

# get version
import beamer_gen
version = beamer_gen.__version__

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name='beamer_gen',
    version=version,
    author='Francis Colas',
    author_email='francis.colas@inria.fr',
    description='Preprocessor to generate LaTeX/beamer files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fcolas/beamer_gen',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Markup :: LaTeX',
    ],
    keywords='LaTeX beamer generator markup',
    python_requires='>=3.4',
    entry_points={
        'console_scripts': [
            'beamer_gen=beamer_gen:main',
        ],
    },
)
