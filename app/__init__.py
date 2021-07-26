import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

def create_app():
    UPLOAD_FOLDER = os.getcwd() + '\\app\\stockage\\'

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
                flash('Pas de fichier selectionné')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('homepage'))
        else:
            return render_template('upload.html')
        
        return

    @app.route('/uploads/<name>')
    def download_file(name):
        return send_from_directory(app.config['UPLOAD_FOLDER'], name)

    @app.route('/list/')
    def list_files():
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('list_files.html', files=files)
    
    @app.route('/delete/')
    def delete():
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('delete_file.html', files=files)

    @app.route('/delete/<name>')
    def delete_file(name):
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], name))
        except FileNotFoundError:
            flash('Fichier non trouvé')
        return redirect(url_for('delete'))

    @app.route('/cli/list')
    def cli_list():
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify(files)

    return app