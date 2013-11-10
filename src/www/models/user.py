import models.base
import utils.utils
import utils.settings


class UserModel(models.base.BaseModel):

    ### Class Variables ###

    ### Private Instance Methods ###
    def __init__(self, app, init_dict=None):
        super(UserModel, self).__init__()
        self._app = app
        self._id = utils.utils.get_attr_or_default(init_dict, 'id')
        self._first_name = utils.utils.get_attr_or_default(init_dict, 'first_name')
        self._last_name = utils.utils.get_attr_or_default(init_dict, 'last_name')
        self._email = utils.utils.get_attr_or_default(init_dict, 'email')
        self._api_token = utils.utils.get_attr_or_default(init_dict, 'api_token')

    ### Properties ###
    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def first_name(self):
        return self._first_name

    @property   
    def api_token(self):
        return self._api_token

    @property
    def flicks(self):
        flick_rows = self._app.mysqldb.query("SELECT * FROM flick WHERE user_id = %s ORDER BY flicked_at DESC", self._id)

        flicks = []

        for flick_row in flick_rows:
            flicks.append(models.flick.FlickModel(self._app, flick_row))

        return flicks

    ### Instance Methods ###


    ### Instance Methods to Implement ###

    ### Class Methods###
    @classmethod
    def get_from_mysql_with_email_and_password(cls, app, email, password):
        hashed_password = password
        init_dict = app.mysqldb.get("SELECT * FROM user WHERE email = %s AND password = %s", email, hashed_password)
        return cls.init_from_app_and_init_dict(app, init_dict)


    @classmethod
    def get_from_mysql_with_id(cls, app, user_id):
        init_dict = app.mysqldb.get("SELECT * FROM user WHERE id=%s", user_id)
        return cls.init_from_app_and_init_dict(app, init_dict)

    @classmethod
    def get_from_mysql_with_api_token(cls, app, api_token):
        init_dict = app.mysqldb.get("SELECT * FROM user WHERE api_token=%s", api_token)
        return cls.init_from_app_and_init_dict(app, init_dict)
    
    ### Class Methods to Implement ###

    ### Static Methods ###

