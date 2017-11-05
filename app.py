from flask import Flask
from extensions import mongo, socket

app = Flask(__name__)

# configuration
app.config['SECRET_KEY'] = '12345'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'minesweeper'

app.config['GAME_MINIMUM'] = {'width': 9, 'height': 9, 'mines': 15}
app.config['GAME_MAXIMUM'] = {'width': 35, 'height': 35, 'mines': 75}
app.config['GAME_OPTIONS'] = [
    {'width': 9, 'height': 9, 'mines': 15},
    {'width': 15, 'height': 15, 'mines': 50},
    {'width': 25, 'height': 25, 'mines': 75}
]


with app.app_context():
    mongo.init_app(app)
    socket.init_app(app)

    from views import view
    app.register_blueprint(view)


if __name__ == '__main__':
    socket.run(app)
