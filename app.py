# from flaskwebgui import FlaskUI
import logging
import socket

from flask_migrate import Migrate

from config.extends import mail, redis, db, socketio
from practice01 import create_app
from flask_cors import CORS

app = create_app()


db.init_app(app)
mail.init_app(app)
redis.init_app(app)
socketio.init_app(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    logging.basicConfig()
    logging.warning('        服务器ip：     ' + ip)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    # FlaskUI(app=app, server="flask", width=1024, height=720).run()
