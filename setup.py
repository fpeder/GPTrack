from distutils.core import setup

setup(
    name='GPTrack',
    version='0.1.0',
    author='Fabrizio Pedersoli',
    author_email='f.peder@gmail.com',
    packages=['gptrack', 'gptrack.test'],
    scripts=['bin/demo.py'],
    # url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Guitar Playing Hands Tracker',
    long_description=open('README.txt').read(),
    install_requires=[
        "scikit-learn",
        "scikit-image",
        "numpy",
        "scipy",
        "cv2"
    ],
)
