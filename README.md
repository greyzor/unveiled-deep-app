# unveiled-deep-app
Discover content in photos using state of the art methods (including deep learning).

## Description
The purpose of this project is to provide an exploration tool for recent deep learning techniques.

Right now, the application currently supports:
* Face detection, based on face_recognition python package (dlib).
* Objects (Tags) recognition in image, based on Inceptionv3 state-of-the-art models.

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

## Related projects
A separate worker executes all tasks related to Inceptionv3. The project is available here: [@greyzor/unveiled-inception-worker](https://github.com/greyzor/unveiled-inception-worker)

## Contributions/Get in Touch
* Please feel free to fork this project or directly pull requests for additional features.
* A nice idea could be to integrate/implement some features provided by Amazon Rekognition service, or equivalent. Cheers :) !