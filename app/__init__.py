import os
from flask import Flask, render_template, request, flash, redirect
from flask.helpers import url_for
from werkzeug.utils import secure_filename

def create_app():
    UPLOAD_FOLDER = os.getcwd() + '\\stockage\\'

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'daf2b3e0858ac96b83b558b1df756da8ede803231124b1fd'

    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/upload/', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('download_file', name=filename))
        else:
            return render_template('upload.html')

    return app