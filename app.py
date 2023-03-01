import time
from absl import app, logging
import cv2
import numpy as np
from flask import Flask, request, Response, jsonify, send_from_directory, abort, render_template,send_file
import os
import sys
from subprocess import call
from detect import *


app = Flask(__name__)
@app.route('/')
def index():
   print('Request for index page received')
   return 'hello world'


@app.route('/image', methods= ['POST'])
def get_image():
   image = request.files['image']
   image.save(image.filename)
   img = detect(image.filename)
   cv2.imwrite('results.png', img)
   os.remove(image.filename)
   return send_file('results.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=5000)
