import time
from absl import app, logging
import cv2
import numpy as np
from flask import Flask, request, Response, jsonify, send_from_directory, abort
import os
import sys
from subprocess import call
from detect import detect


def run_cmd(command):
        try:
            call(command, shell=True)
        except KeyboardInterrupt:
            print("Process interrupted")
            sys.exit(1)

# Initialize Flask application
app = Flask(__name__)
@app.route('/')
def home():
    return 'flask web app'

# API that returns image with detections on it
@app.route('/image', methods= ['POST'])
def get_image():
    image = request.files["images"]
    image_name = image.filename
    image.save(os.path.join(os.getcwd(), image_name))

    t1 = time.time()
    img=detect(image_name)
    t2 = time.time()
    print('time: {}'.format(t2 - t1))

    print('detections:')
    cv2.imwrite('results.png', img)
    print('output saved to: {}'.format('results.png'))
    
    # prepare image for response
    _, img_encoded = cv2.imencode('.png', img)
    response = img_encoded.tostring()
    
    #remove temporary image
    os.remove(image_name)

    try:
        return Response(response=response, status=200, mimetype='image/png')
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run()