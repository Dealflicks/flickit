import models.base
import utils.utils
import utils.settings
import models.movie


class FlickModel(models.base.BaseModel):

    ### Class Variables ###

    ### Private Instance Methods ###
    def __init__(self, app, init_dict=None):
        super(FlickModel, self).__init__()
        self._app = app
        self._id = utils.utils.get_attr_or_default(init_dict, 'id')
        self._flicked_at = utils.utils.get_attr_or_default(init_dict, 'flicked_at')
        self._movie_id = utils.utils.get_attr_or_default(init_dict, 'movie_id')
        self._user_id = utils.utils.get_attr_or_default(init_dict, 'user_id')


    ### Properties ###
    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def movie(self):
        return utils.movie.MovieModel.get_from_mysql_with_id(self._app, self._movie_id)


    ### Instance Methods ###


    ### Instance Methods to Implement ###

    ### Class Methods###
    @classmethod
    def get_or_create(cls, app, movie_id, user_id):
        flick = cls.get_from_mysql_with_movie_id_and_user_id(app, movie_id, user_id)

        if not flick:
            flick_id = app.mysqldb.execute("INSERT INTO flick (movie_id, user_id, flicked_at) VALUES (%s, %s, UTC_TIMESTAMP())", movie_id, user_id)
            flick = cls.get_from_mysql_with_id(app, flick_id)
        
        return flick


    @classmethod
    def get_from_mysql_with_id(cls, app, flick_id):
        init_dict = app.mysqldb.get("SELECT * FROM flick WHERE id=%s", flick_id)
        return cls.init_from_app_and_init_dict(app, init_dict)
    

    @classmethod
    def get_from_mysql_with_movie_id_and_user_id(cls, app, movie_id, user_id):
        init_dict = app.mysqldb.get("SELECT * FROM flick WHERE movie_id=%s AND user_id=%s", movie_id, user_id)
        return cls.init_from_app_and_init_dict(app, init_dict)
  
    ### Class Methods to Implement ###

    ### Static Methods ###

