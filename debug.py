from logging import debug

from flask.json.tag import TagMarkup
import app

app.create_app().run(debug=True)