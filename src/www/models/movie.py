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
        self._dealflicks_id = utils.utils.get_attr_or_default(init_dict, 'dealflicks_id')
        self._poster = utils.utils.get_attr_or_default(init_dict, 'poster')
        self._critics_score = utils.utils.get_attr_or_default(init_dict, 'critics_score')
        self._audience_score = utils.utils.get_attr_or_default(init_dict, 'audience_score')
        self._duration = utils.utils.get_attr_or_default(init_dict, 'duration')
        self._mpaa_rating = utils.utils.get_attr_or_default(init_dict, 'mpaa_rating')
        self._genre = utils.utils.get_attr_or_default(init_dict, 'genre')
        self._abridged_cast = utils.utils.get_attr_or_default(init_dict, 'abridged_cast')
        self._synopsis = utils.utils.get_attr_or_default(init_dict, 'synopsis')
        self._theater_release_date = utils.utils.get_attr_or_default(init_dict, 'theater_release_date')
        self._rotten_tomatoes_id = utils.utils.get_attr_or_default(init_dict, 'rotten_tomatoes_id')

    ### Properties ###
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def dealflicks_id(self):
        return self._dealflicks_id

    @property
    def poster(self):
        return self._poster

    @property
    def critics_score(self):
        return self._critics_score

    @property
    def audience_score(self):
        return self._audience_score

    @property
    def duration(self):
        return self._duration

    @property
    def mpaa_rating(self):
        return self._mpaa_rating

    @property
    def genre(self):
        return self._genre

    @property
    def abridged_cast(self):
        return self._abridged_cast

    @property
    def synopsis(self):
        return self._synopsis

    @property
    def theater_release_date(self):
        return self._theater_release_date

    @property
    def rotten_tomatoes_id(self):
        return self._rotten_tomatoes_id

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

