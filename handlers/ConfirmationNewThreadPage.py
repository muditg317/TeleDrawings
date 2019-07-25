import webapp2
import jinja2
import os
import random
from google.appengine.api import users,images
from models import ThreadContent,Drawing,Caption,TeleUser,Thread,Edit

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/../templates/"),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

class ConfirmationNewThreadPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/welcome")

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect("/welcome")
        else:
            teleUser = TeleUser.get_by_id(user.user_id())
            if not teleUser:
                teleUser = TeleUser.fromGSI(user=user)
                teleUser.put()
            thread_id = random.randint(1000000000,9999999999)
            thread = Thread(thread_id=thread_id)
            drawing = self.request.get("drawing")
            size = 600;
            drawing = images.resize(drawing,size,size)
            new_drawing = Drawing(content=drawing)
            content_key = new_drawing.put()
            thread.drawings.append(content_key)
            thread_key = thread.put()
            new_edit = Edit(user=teleUser.key,thread=thread_key,addition=content_key)
            new_edit.put()
            confirmation_newThread_template = the_jinja_env.get_template("confirmation-newthread.html")
            self.response.write(confirmation_newThread_template.render({
                "user_info":user,
                "thread":thread,
                "new_edit":new_edit
            }))