import tornado.web

import handlers.base


class WidgetBuilderHandler(handlers.base.BaseHandler):

    def get(self):
   
        self.render("widget_builder.html")
