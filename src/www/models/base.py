import utils.utils

"""Classes should be structered as follows

Example subclass:

    class Model(models.BaseModel):

        ### Class Variables ###
        title = "Item"

        ### Private instance Methods ###
        def __init__(app, init_dict=None):

            # call super first
            super(Model, self).__init__()

            # for models used within in application, we always set self._app
            self._app = app

            # use utils.utils.get_attr_or_default to retrieve value from dict
            self._quantity = utils.utils.get_attr_or_default(init_dict, 'quantity', default=0)

            # use hasattr to ensure that a class variable is implemented
            if not hasattr(self, 'title'):
                raise NotImplementedError("title")

        ### Properties ###

        # use @property decorator
        @property
        def quantity(self):
            return self._quantity

        # only implement setter if necessary
        @quantity.setter
        def quantity(self, value):
            self._quantity = value

        # do not implement deleters
 

        ### Instance Methods ###

        def add(self, addend):
            self._quantity += addend

        ### Instance Methods to Implement

        # raise NotImplementedError to ensure subclasses overrides
        def render(self):
            raise NotImplementedError


        ### Class Methods ####

        # typically only use class methods for constructors
        # when retrieving from a db, ensure the db type is defined (mysqldb or redis for now)
        def get_from_mysql_with_id(cls, app, id):
            init_dict = cls.select_from_mysql_with_id(app, id)
            return cls(app, init_dict=init_dict)


        ### Class Methods to Implement ###

        # raise NotImplementedError to ensure subclasses override
        def select_from_mysql_with_id(app, id):
            raise NotImplementedError

        ### Static Methods ####

        # methods that you want every subclass to have
        def pluralize(singular_word):
            pass


Notes: 

    * You should not define factory static methods here. When you import a 
      subclass, you'll get a circular reference problem.  Instead, create a 
      separate factory class in a different file.

    * never use "from module import class"  this can cause scoping issues

    * always use the full module path, e.g., "models.base.BaseModel"

    * if you're trying to instantiate a model based on same values,
      then define the method as a class method not a static method.

"""


class BaseModel(object):
    
    ### Class Variables ###

    ### Private Instance Methods ####

    def __init__(self):
        pass

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%r" % self.__dict__
   

    ### Properties ###

    ### Instance Methods ###

    ### Instance Methods to Implement ###

    ### Class Methods ###

    # TODO rename... used in an attempt to keep things DRY
    @classmethod
    def init_from_app_and_init_dict(cls, app, init_dict):
        """
            Helper function that will return None if init_dict is None
        """
        if init_dict is not None:
            return cls(app, init_dict=init_dict)
        else:
            return None   

    ### Class Methods to Implement ###

    ### Static Methods ####


  
