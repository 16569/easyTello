import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='easytello',
    version='0.0.7',
    author='16569',
    author_email='osamu_cyber@me.com',
    description='An easy framework to support DJI Tello scripting in Python 3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/16569/easyTello',
    packages=setuptools.find_packages(),
    install_requires=[
        'opencv-python'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)