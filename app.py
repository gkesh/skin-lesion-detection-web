from quart import Quart
from quart_uploads import configure_uploads
from quart_schema import QuartSchema

from uploads import images
from routes import api, web

import os


app = Quart(__name__)

QuartSchema(app)

# Adding pug middleware
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

# Setting up image set
app.config['UPLOADED_IMAGES_DEST'] = f"{os.getcwd()}/static/img/uploads"
configure_uploads(app, images)

# Setting up API backend
app.register_blueprint(api)
app.register_blueprint(web)
