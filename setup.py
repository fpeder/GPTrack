from distutils.core import setup

setup(
    name='GPTrack',
    version='0.1.2',
    author='Fabrizio Pedersoli',
    author_email='f.peder@gmail.com',
    packages=['gptrack', 'gptrack.skin', 'gptrack.hands', 'gptrack.seq'],
    #scripts=['bin/demo.py'],
    # url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Guitar Playing Hands Tracker',
    long_description=open('README.txt').read(),
    install_requires=[
        "scikit-learn",
        #"scikit-image",
        "numpy",
        "scipy",
        "cv2"
    ],
)
