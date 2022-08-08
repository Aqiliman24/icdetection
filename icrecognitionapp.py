
from cgitb import html
from keras.models import load_model
from flask import *
from PIL import Image
from sqlalchemy import false, true
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import easyocr
import os

model = load_model('icrecognition.h5')

classes = {
    0 : 'No Pain',
    1 : 'Pain'
}

def textprocessing(img):
   
    print (img)
    img = cv2.imread(img)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0, sigmaY=0) #Bluring image in a small amount
    filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) # Creating our sharpening filter

    sharpen_img = cv2.filter2D(gray,-1,filter) # Applying cv2.filter2D sharpening function on image

    reader = easyocr.Reader(['en'])
    result = reader.readtext(sharpen_img)

    result_val = " "
    for x in result:
        result_val += (x[1]+",")

    result_val.strip()

    return (result_val)


# main -----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
print ("Hello")
@app.route("/", methods=['GET', 'POST'])
def summary():
    uploads_dir = os.path.join('')
    ic = request.files['ic']
    
    
    if ic != '':
        image = Image.open(ic)
        image = image.convert("RGB")
        image.save(os.path.join(uploads_dir, secure_filename("uploadedimage.jpg")))
        resizeimage = image.resize((200,200))
        resizeimage = np.expand_dims(resizeimage, axis = 0)
        resizeimage = np.array(resizeimage)
        pred = model.predict([resizeimage])[0]
        icpath = 'uploadedimage.jpg'
        icpath = str(icpath)
        dataic = textprocessing(icpath)

        if (pred == 0):
            data = {
                "status" : bool(true),
                "extraction" : dataic

            }
        else:
            data = {
                "status" : bool(false)
            }

        os.remove(icpath)
        return jsonify(data)

    else:
        return ('error')


if __name__ == '__main__':   
    app.run(host = '0.0.0.0',port=8001,debug=True)
    
# main ----------------------------------------------------------------------------------------------------------------------------