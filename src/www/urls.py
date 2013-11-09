import handlers.home 
import handlers.auth
import handlers.flicks


handlers = [

      (r"/", handlers.home.HomeHandler),
      (r"/login", handlers.auth.AuthLoginHandler),
      (r"/flicks", handlers.flicks.FlicksHandler)

]

