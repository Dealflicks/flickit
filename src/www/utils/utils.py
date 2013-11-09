def get_attr_or_default(unidentified_object, attr_name, default_value=None):
    if type(unidentified_object) == dict:
        return unidentified_object.get(attr_name, default_value)
    else:
        try:
            return getattr(unidentified_object, attr_name, default_value)
        except Exception, e:
            return default_value