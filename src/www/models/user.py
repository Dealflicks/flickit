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

    ### Properties ###
    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

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
    
    ### Class Methods to Implement ###

    ### Static Methods ###

