import models.base
import utils.utils
import utils.settings


class MovieModel(models.base.BaseModel):

    ### Class Variables ###

    ### Private Instance Methods ###
    def __init__(self, app, init_dict=None):
        super(MovieModel, self).__init__()
        self._app = app
        self._id = utils.utils.get_attr_or_default(init_dict, 'id')
        self._name = utils.utils.get_attr_or_default(init_dict, 'name')

    ### Properties ###
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        count_dict = self._app.mysqldb.get("SELECT count(*) AS flick_count FROM flick WHERE movie_id=%s", self._id)
        return count_dict['flick_count']


    ### Instance Methods ###


    ### Instance Methods to Implement ###

    ### Class Methods###
    @classmethod
    def get_from_mysql_with_id(cls, app, movie_id):
        init_dict = app.mysqldb.get("SELECT * FROM movie WHERE id=%s", movie_id)
        return cls.init_from_app_and_init_dict(app, init_dict)
    
    ### Class Methods to Implement ###

    ### Static Methods ###

