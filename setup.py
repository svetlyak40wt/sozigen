from distutils.core import setup

setup(
    name='sozigen',
    version='0.1.0',
    packages=['sozigen'],
    license='New BSD License',
    long_description=open('README.md').read().decode('utf-8'),
    package_data={'sozigen': ['custom.js', 'sozi.js', 'template.xml']},
    url='http://svetlyak40wt.github.com/sozigen/',
    author='Alexander Artemenko',
    author_email='svetlyak.40wt@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
