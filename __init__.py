from flask import Flask, render_template, flash, request, redirect, jsonify
from werkzeug import routing
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename
import cv2 as cv
import numpy as np
import os

from AStar import AStar
from utils import Plotting

def route_(app: Flask) -> routing.Map:
    @app.route('/', methods=['GET'])
    def index():
        return render_template("index.html", canvas_dim = app.config['CANVAS_DIM'], h_methods = app.config['H_METHODS'])
    
    def save_file(file: FileStorage) -> str:
        if file.filename == '':
            flash('No selected file')
            return ''
            # return redirect(request.url)
        
        filename: str = secure_filename(file.filename)
        upload_folder: str = app.config['UPLOAD_FOLDER']
        
        # make directory if doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # save image
        save_path: str = os.path.join(upload_folder, filename)
        file.save(save_path)

        return save_path

    # TODO: Make faster by not requiring upload of file *MAJOR CHANGE
    @app.route('/get_path', methods=['POST'])
    def get_path():
        if 'upload' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        
        h_method: str = request.form.get('h_method')
        
        file = request.files['upload']
        save_path: str = save_file(file)

        a: AStar = app.config['ASTAR']
        p: Plotting = app.config['PLOTTER']

        grid, src, dest = p.from_image(save_path)
        path: np.ndarray = np.array(a.search(grid, src, dest, h_method=h_method))
        
        return jsonify(path.tolist())

    return app.url_map


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config['CANVAS_DIM'] = {'width': 500, 'height': 500}
    app.config['UPLOAD_FOLDER'] = './mazes'
    app.config['ASTAR'] = AStar(**app.config['CANVAS_DIM'])
    app.config['PLOTTER'] = Plotting()
    app.config['H_METHODS'] = {"euclidean" : "$$\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$$", 
                               "manhattan" : "$$|x_2-x_1| + |y_2-y_1|$$", 
                               "chebyshev" : "$$max(|x_2-x_1|, |y_2-y_1|)$$"
                              }
    
    route_(app)
    
    return app