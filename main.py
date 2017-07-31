import os

from flask import Flask, jsonify
from flask_restful import Api

from api.views.articles_by_topic import ArticlesByTopicResource
from api.views.get_topics import GetTopicsResource
from config import app_configuration


def create_flask_app(environment):
    # initialize Flask
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(app_configuration[environment])

    # test route
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Punch Nigeria Api"})

    # create endpoints
    api = Api(app)
    api.add_resource(ArticlesByTopicResource, '/api/v1/articles',
                     endpoint='articles_by_topic')
    api.add_resource(GetTopicsResource, '/api/v1/topics',
                     endpoint='get_topics')

    # handle default 404 exceptions with a custom response
    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify(dict(status=404, error='Not found', message='The '
                                'requested URL was not found on the server. If'
                                ' you entered the URL manually please check '
                                'your spelling and try again'))
        response.status_code = 404
        return response

    # handle default 500 exceptions with a custom response
    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify(dict(status=500, error='Internal server error',
                                message="It is not you. It is me. The server "
                                "encountered an internal error and was unable "
                                "to complete your request.  Either the server "
                                "is overloaded or there is an error in the "
                                "application"))
        response.status_code = 500
        return response

    return app


# enable the flask run command to work
app = create_flask_app(os.getenv("FLASK_CONFIG"))


if __name__ == "__main__":
    environment = os.getenv("FLASK_CONFIG")
    app = create_flask_app(environment)
    app.run()
