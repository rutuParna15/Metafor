from flask import Flask

def create_app():
    app = Flask(__name__)
        
    from .routes import routes
    from .controllers import controllers

    app.register_blueprint(routes)
    app.register_blueprint(controllers)
    
    return app