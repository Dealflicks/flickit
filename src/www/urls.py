import handlers.home 
import handlers.auth
import handlers.flicks
import handlers.api
from handlers.imagesearch import PictureSearchHandler, PictureSearchByStringHandler, ImageSearchHandler


handlers = [

      (r"/", handlers.home.HomeHandler),
      (r"/login", handlers.auth.AuthLoginHandler),
      (r"/flicks", handlers.flicks.FlicksHandler),
      (r"/flicks/create", handlers.flicks.FlicksCreateHandler),
      (r"/api/v1/flicks/count\.json", handlers.api.FlickCountHandler),
      (r"/api/v1/flicks/create\.json", handlers.api.FlickCreateHandler),

      (r"/picture-search", PictureSearchHandler),
      (r"/picture-string-search", PictureSearchByStringHandler),
      (r"/image-search/imgurl\.json", ImageSearchHandler)

]

