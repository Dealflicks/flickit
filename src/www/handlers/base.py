import tornado.web
import tornado.escape

import utils.validationmixin

import uuid

class BaseHandler(tornado.web.RequestHandler, utils.validationmixin.ValidationMixin):
    @property
    def mysqldb(self):
        return self.application.mysqldb

    def check_xsrf_cookie(self):
        pass

    def write_error(self, status_code, **kwargs):

        if 'chunk' in kwargs:
            self.write(kwargs['chunk'])

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


