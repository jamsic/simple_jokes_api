from flask import abort
from models import session, UserModel
from sqlalchemy.orm.exc import NoResultFound


class SimpleAuthorizer:

    def authorize_user(self, auth_username, url_user_id):
        try:
            this_user = session.query(UserModel)
            this_user = this_user.filter(UserModel.id_ == url_user_id).one()
            if this_user.username != auth_username:
                abort(403, 'forbidden')
            return this_user
        except NoResultFound:
            abort(403, 'forbidden')

