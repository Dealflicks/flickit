import tornado.web
import tornado.escape

import utils.validationmixin

import uuid

import models.user

class BaseHandler(tornado.web.RequestHandler, utils.validationmixin.ValidationMixin):
    @property
    def mysqldb(self):
        return self.application.mysqldb

    def check_xsrf_cookie(self):
        pass

    def write_error(self, status_code, **kwargs):

        if 'chunk' in kwargs:
            self.write(kwargs['chunk'])

    def get_current_user(self):
        # normal web request
        user_cookie = self.get_secure_cookie("user")
        if not user_cookie:
            return None
        user_dict = tornado.escape.json_decode(user_cookie)

        return models.user.UserModel.get_from_mysql_with_id(self.application, user_dict['id'])

    def render_json(self, chunk):
        if isinstance(chunk, dict):
            dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
            chunk = json.dumps(chunk, default=dthandler)
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        chunk = tornado.escape.utf8(chunk)
        self._write_buffer.append(chunk)

    def render(self, template_name, **kwargs):
        if (self.request.headers.get("Mime-Type") == "json"):
            self.render_json(kwargs)
        else:
            super(BaseHandler, self).render(template_name, **kwargs)


