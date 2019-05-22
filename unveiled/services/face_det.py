"""
"""
import face_recognition
from PIL import Image
import os
import uuid
import cv2

def find_face_locations(file_stream, out_dir=None):
    """ """
    # Load the uploaded image file
    image = face_recognition.load_image_file(file_stream)

    face_locations = face_recognition.face_locations(image)
    print("I found {} face(s) in this photograph.".format(len(face_locations)))

    cropped_images = []
    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        #######################################################################
        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        cropped_img = Image.fromarray(face_image)
        if out_dir is not None:
            cropped_id = uuid.uuid4().hex
            fname = 'cropped-{img_id}.jpg'.format(img_id=cropped_id)
            fpath = os.path.join(out_dir, fname)
            cropped_img.save(fpath)
            print('Saving cropped to: %s' % fpath)
            cropped_images.append(fname)

    #######################################################################
    # Show rectangles and legend
    for k, face_location in enumerate(face_locations):
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        face_name = 'Face #%d' % k

        # Draw a box around the face
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, face_name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    img_id = uuid.uuid4().hex
    img_src = 'annot-{img_id}.jpg'.format(img_id=img_id)
    fpath = os.path.join(out_dir, img_src)
    Image.fromarray(image).save(fpath)
    print('Saving final image to: %s' % fpath)

    return {
        "face_locations": face_locations,
        "cropped_imgs": cropped_images,
        "img_src": img_src # modified image path
    }