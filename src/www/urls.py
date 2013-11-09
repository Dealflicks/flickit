import handlers.home 


handlers = [
      # landing pages
      (r"/", handlers.home.HomeHandler)
]

