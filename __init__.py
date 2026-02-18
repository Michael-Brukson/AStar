from flask import Flask, render_template, flash, request, redirect
from werkzeug import routing
from werkzeug.utils import secure_filename
import os

import AStar
from utils import Plotting

def route_(app: Flask) -> routing.Map:
    @app.route('/', methods=['GET'])
    def index():
        return render_template("index.html")
    

    @app.route('/upload', methods=['POST'])
    def upload():
        if 'upload' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['upload']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        filename: str = secure_filename(file.filename)
        upload_folder: str = app.config['UPLOAD_FOLDER']
        
        # make directory if doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # save image
        file.save(os.path.join(upload_folder, filename))
        return 'File uploaded successfully', 200
    

    return app.url_map


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = './mazes'
    
    route_(app)
    
    return app