import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify, abort
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user

db = SQLAlchemy()

def create_app():
    UPLOAD_FOLDER = os.getcwd() + '\\wfti\\stockage\\'

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'daf2b3e0858ac96b83b558b1df756da8ede803231124b1fd'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/upload/', methods=['GET', 'POST'])
    @login_required
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
                user = User.query.get(current_user.id)
                if user.files:
                    user.files = str(user.files) + filename + "|"
                else:
                    user.files = filename + "|"
                db.session.commit()
                return redirect(url_for('homepage'))
        else:
            return render_template('upload.html')

    @app.route('/uploads/<name>')
    @login_required
    def download_file(name):
        if name not in current_user.files:
            abort(404)
        return send_from_directory(app.config['UPLOAD_FOLDER'], name)

    @app.route('/list/')
    @login_required
    def list_files():
        if current_user.files:
            files = current_user.files.split("|")
            files.pop()
        else:
            files = list()
        return render_template('list_files.html', files=files)
    
    @app.route('/delete/')
    @login_required
    def delete():
        if current_user.files:
            files = current_user.files.split("|")
            files.pop()
        else:
            files = list()
        return render_template('delete_file.html', files=files)

    @app.route('/delete/<name>')
    @login_required
    def delete_file(name):
        if name not in current_user.files:
            abort(404)
        else:
            user = User.query.get(current_user.id)
            user.files = user.files.replace(name + "|", "")
            db.session.commit()
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], name))
        except FileNotFoundError:
            flash('Fichier non trouvé')
        return redirect(url_for('delete'))

    @app.route('/404/')
    def QCQ():
        abort(404)

    @app.errorhandler(404)
    def page_not_found(error):
        return "Page non trouvé | " + str(error), 404

    @app.errorhandler(500)
    def error500(error):
        return "C'est la merde | " + str(error), 500

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', name=current_user.name)

    return app