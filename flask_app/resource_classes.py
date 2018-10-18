from flask import jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource
from geek_jokes_api import GeekJokesApi
from logger import Logger
from models import session, UserModel, JokeModel
from sqlalchemy.orm.exc import NoResultFound
from .simple_authorizer import SimpleAuthorizer


auth = HTTPBasicAuth()
geek_jokes = GeekJokesApi()
logger = Logger()
authorizer = SimpleAuthorizer()


@auth.verify_password
def verify_pw(username, password):
    try:
        user = session.query(UserModel)
        user = user.filter(UserModel.username == username).one()
        return user.check_password(password)
    except NoResultFound as e:
        pass
    return False


class Users(Resource):

    def post(self):
        content = request.json
        if not content:
            abort(400, 'username and password data is required')
        username = content.get('username')
        password = content.get('password')
        if not password or not username:
            abort(400, 'username and password are mandatory')
        user = session.query(UserModel)
        user = user.filter(UserModel.username == username).first()
        if user is not None:
            abort(409, 'user already exists')
        new_user = UserModel(username=username)
        new_user.hash_password(password)
        session.add(new_user)
        session.commit()
        logger.log(new_user.username, request.date, request.remote_addr,
                   request.url)
        return make_response(jsonify(user=new_user.serialize), 201)


class User(Resource):

    @auth.login_required
    def get(self, account_id):
        logger.log(auth.username(), request.date, request.remote_addr,
                   request.url)
        authorized_user = authorizer.authorize_user(auth.username(),
                                                    account_id)
        return jsonify(user=authorized_user.serialize)


class Jokes(Resource):

    POST_GENERATION_RETRY_TIMES = 10

    @auth.login_required
    def get(self, account_id):
        logger.log(auth.username(), request.date, request.remote_addr,
                   request.url)
        authorizer.authorize_user(auth.username(), account_id)
        jokes = session.query(JokeModel)
        jokes = jokes.join(UserModel, JokeModel.user_id == UserModel.id_)
        jokes = jokes.filter(JokeModel.user_id == account_id).all()
        return jsonify(jokes=[j.serialize for j in jokes])

    @auth.login_required
    def post(self, account_id):
        logger.log(auth.username(), request.date, request.remote_addr,
                   request.url)
        authorizer.authorize_user(auth.username(), account_id)
        joke_cnt = None
        for i in xrange(self.POST_GENERATION_RETRY_TIMES):
            new_joke_text = geek_jokes.get_a_joke()
            if not new_joke_text:
                abort(500)
            joke_cnt = session.query(JokeModel)
            joke_cnt = joke_cnt.filter(JokeModel.text == new_joke_text).count()
            if joke_cnt == 0:
                break
        else:
            abort(500)
        new_joke = JokeModel(text=new_joke_text, user_id=account_id)
        session.add(new_joke)
        session.commit()
        return make_response(jsonify(joke=new_joke.serialize), 201)


class Joke(Resource):

    def get_joke_or_404(self, joke_id, account_id):
        try:
            joke = session.query(JokeModel)
            joke = joke.filter(JokeModel.id_ == joke_id).one()
            if joke.user_id != account_id:
                abort(404)
            return joke
        except NoResultFound as e:
            abort(404, 'joke not found')

    @auth.login_required
    def get(self, account_id, joke_id):
        logger.log(auth.username(), request.date, request.remote_addr,
                   request.url)
        authorizer.authorize_user(auth.username(), account_id)
        joke = self.get_joke_or_404(joke_id, account_id)
        return jsonify(joke=joke.serialize)

    @auth.login_required
    def put(self, account_id, joke_id):
        logger.log(auth.username(), request.date, request.remote_addr,
                   request.url)
        authorizer.authorize_user(auth.username(), account_id)
        json_obj = request.json
        if 'text' not in json_obj or not json_obj['text']:
            abort(400)
        joke = self.get_joke_or_404(joke_id, account_id)
        joke.text = json_obj['text']
        session.add(joke)
        session.commit()

    @auth.login_required
    def delete(self, account_id, joke_id):
        logger.log(auth.username(), request.date, request.remote_addr,
                   request.url)
        authorizer.authorize_user(auth.username(), account_id)
        joke = self.get_joke_or_404(joke_id, account_id)
        session.delete(joke)
        session.commit()

