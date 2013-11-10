import handlers.home 
import handlers.auth
import handlers.flicks
import handlers.api
from handlers.imagesearch import PictureSearchHandler, PictureSearchByStringHandler, ImageSearchHandler
import handlers.widget_builder


handlers = [

      (r"/", handlers.home.HomeHandler),
      (r"/login", handlers.auth.AuthLoginHandler),
      (r"/flicks", handlers.flicks.FlicksHandler),
      (r"/widget-builder", handlers.widget_builder.WidgetBuilderHandler),
      (r"/flicks/create", handlers.flicks.FlicksCreateHandler),
      (r"/api/v1/flicks/count\.json", handlers.api.FlickCountHandler),
      (r"/api/v1/flicks/create\.json", handlers.api.FlickCreateHandler),
      (r"/api/v1/flicks/create-from-imgurl\.json", ImageSearchHandler),

      (r"/picture-search", PictureSearchHandler),
      (r"/picture-string-search", PictureSearchByStringHandler),

]

