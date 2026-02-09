from flask import Flask, render_template
from werkzeug import routing

def route_(app: Flask) -> routing.Map:
    @app.route('/', methods=['GET'])
    def index():
        return render_template("index.html")
    
    return app.url_map


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    
    route_(app)
    
    return app