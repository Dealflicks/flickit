import tornado.web

import handlers.base

import models.user

import utils.validationmixin


class AuthLoginHandler(handlers.base.BaseHandler):

    def finish_login(self, user, redirect_url):
        user_id = user.id
        self.set_secure_cookie("user", tornado.escape.json_encode({'id' : user.id }))
        # redirect_url = self.get_cookie('redirect_after_login')

        if redirect_url is None:
            redirect_url = '/'

        self.redirect(redirect_url)


    def get(self):
        next_url = self.get_argument('next', '/')
        
        self.render("login.html", next_url=next_url)

    def post(self): 
        email = self.valid("email", utils.validationmixin.ValidationMixin.EMAIL)
        password = self.valid("password")
        redirect_url =  self.get_argument("next", u"/")

        print redirect_url

        if (self.errors):
            return self.send_error(400, chunk={'Status' : 'Error', 'Errors' : self.errors })

        user =  models.user.UserModel.get_from_mysql_with_email_and_password(self.application, email, password)

        # validate that the login works
            
        if user:
            self.finish_login(user, redirect_url)
            # return self.write({'Status' : 'OK', 'user_id' : user.id, 'api_token' : user.api_token,'redirect_url' : self.get_cookie('redirect_after_login')})
        else:
            return self.send_error(400, chunk={'Status' : 'Error', 'Errors' : {'alert' : 'Bad login. Email or password is incorrect.'} })
