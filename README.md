# unveiled-deep-app
Discover content in photos using state of the art methods (including deep learning).

## Description
The purpose of this project is to provide an exploration tool for recent deep learning techniques.

Right now, the application currently supports:
* Face detection, based on face_recognition python package (dlib).

## Preview
A demo is available here: [unveiled-app.herokuapp.com/](https://unveiled-app.herokuapp.com/)

## Installation
```
python3 -m pip install -r requirements.txt
```

## Run locally
```
python3 manage.py run
```

## Limitations
Currently, detection accuracy is not very precise on face detection for unknown images. The model may need to be retrained and more robust for vector simple transforms (faces rotated/translated).

## Get in Touch
Please feel free to fork this project or directly pull requests for additional features.