import os
import json
from flask import Flask, request, redirect, url_for, flash, send_from_directory, render_template
from werkzeug.utils import secure_filename
from werkzeug.wsgi import get_input_stream

from Aplicacio import fins_ingr_princ, fins_resultat
from io import BytesIO

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



# def upload_file():
#     if 'file' in request.files:
#         file = request.files['file']
#         if file.filename != '':
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 file.save(path)
#                 json = fins_ingr_princ(path)
#                 return "funciona"

    # Si actives aquesta part i desactives la part superior, funciona en una web fins a la pregunta. Utilitzant Flask
@app.route('/upload-form', methods=['POST'])
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
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            json = fins_ingr_princ(path)
            return json
            # return render_template('pregunta.html', var1=json)


@app.route('/upload', methods=['POST', 'PUT'])
def upload_file():
    # request.shallow = True
    filename = "picture.jpg"
    fileFullPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(fileFullPath, 'wb+') as f:
        # request.environ['CONTENT_TYPE'] = 'application/something_Flask_ignores'
        # print("cosa: ", request.environ['CONTENT_TYPE'])
        input = get_input_stream(request.environ, safe_fallback=False).read()
        print("Input: ", input)
        f.write(input)
    json_ingredients = fins_ingr_princ(fileFullPath)
    return json_ingredients
    # return "A"

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')


@app.route('/ingredients', methods=['POST'])
def ingredients():
    json_data = request.form['ingredients']
    ingredients = json.loads(json_data)
    ingredient_princ = ingredients[0]
    ingredients_sec = []
    for x in range(len(ingredients)):
        if x != 0:
            ingredients_sec.append(ingredients[x])
    json_resultat = fins_resultat(ingredient_princ, ingredients_sec)
    return json_resultat

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get("PORT", 5000)))
