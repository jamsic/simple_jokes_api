from flask import Flask, jsonify, request, abort
from flask_restful import Api
from resource_classes import Users, User, Jokes, Joke
from models import session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'


@app.teardown_request
def remove_session(ex=None):
    session.remove()

api = Api(app)
api.add_resource(Users, '/v1/users')
api.add_resource(User, '/v1/users/<int:account_id>')
api.add_resource(Jokes, '/v1/users/<int:account_id>/jokes')
api.add_resource(Joke, '/v1/users/<int:account_id>/jokes/<int:joke_id>')

if __name__ == '__main__':
    app.run(debug=True)

