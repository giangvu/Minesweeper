from flask import Flask, render_template
from extensions import mongo, socket

app = Flask(__name__)

# configuration
app.config['SECRET_KEY'] = 'apw#%17fe39^&@.'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'minesweeper'

app.config['GAME_MINIMUM'] = {'width': 10, 'height': 10, 'mines': 20}
app.config['GAME_MAXIMUM'] = {'width': 35, 'height': 15, 'mines': 100}
app.config['GAME_OPTIONS'] = [
    {'width': 10, 'height': 10, 'mines': 20},
    {'width': 18, 'height': 15, 'mines': 50},
    {'width': 25, 'height': 15, 'mines': 75}
]


with app.app_context():
    mongo.init_app(app)
    socket.init_app(app)

    from views import view
    app.register_blueprint(view)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    socket.run(app)
