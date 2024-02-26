from setuptools import setup, find_packages

setup(
    name='voting_web',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'Django',
        'numpy',
        'openpyxl',
        'deepface',
        'face_recognition',
        'opencv-python',
        'distlib',
        'dlib',
        'keras',
        'opencv-contrib-python',
        'oauthlib',
        'opencv-python',
        'tensorflow',
        'tqdm'
    ],
)
