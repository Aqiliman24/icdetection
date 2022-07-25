
from keras.models import load_model
from flask import *
from PIL import Image
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import numpy

model = load_model('icrecognition.h5')

classes = {
    0 : 'No Pain',
    1 : 'Pain'
}


# main -----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
@app.route("/icrecognition", methods=['GET', 'POST'])
def summary():
    # uploads_dir = os.path.join('uploads')
   
    ic = request.files['ic']
    print (type(ic))
    # ic.save(os.path.join(uploads_dir, secure_filename(ic.filename)))
    if ic != '':
        image = Image.open(ic)
        image = image.resize((200,200))
        image = numpy.expand_dims(image, axis = 0)
        image = numpy.array(image)
        pred = model.predict([image])[0]

        if (pred == 0):
            sign = "Success"
            print(sign)
        else:
            sign = "Wrong Identification card. Please try again!"
            print(sign)
            
        return (sign)

if __name__ == '__main__':   
    app.run(host = '0.0.0.0',port=5000,debug=True)
    # main -----------------------------------------------------------------------------------------------------------------------------