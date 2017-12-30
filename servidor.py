# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, flash, send_from_directory, render_template
from werkzeug.utils import secure_filename
from aplicacio import fins_ingr_princ, fins_resultat
from PIL import Image
import uuid

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/icon/<filename>')
def icon(filename):
    return send_from_directory('icon',
                               filename)


@app.route('/upload', methods=['GET'])
def upload():
    return render_template('resultat.html')


@app.route('/upload-image', methods=['POST'])
def upload_file_form():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            typefile = filename.split('.')[1]
            filename = str(uuid.uuid4()) + '.' + typefile
            path = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(path)
            im = Image.open(path)
            im.thumbnail((1000, 1000), Image.ANTIALIAS)
            im.save(path)
            llista_ingr = fins_ingr_princ(path)
            return render_template('pregunta.html', llista_ingr=llista_ingr, filename=filename)


@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')


@app.route('/upload-ingredient')
def upload_ingredient():
    filename = request.args.get('filename')
    ingredient_principal = request.args.get('ingredient_principal')
    ingredients_sec=[]
    for x in request.args.get('ingredients').split(","):
        if x != ingredient_principal:
            ingredients_sec.append(x)
    kcal, fat, carb = fins_resultat(ingredient_principal, ingredients_sec)
    return render_template('resultat.html', kcal=kcal, fat=fat, carb=carb, filename=filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get("PORT", 5000)))
