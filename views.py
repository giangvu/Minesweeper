from flask import Blueprint, request, render_template, redirect, url_for, current_app as app, jsonify, abort
from db_connector import DatabaseConnector as database
from game_factory import GameFactory
from game import Game
from forms import GameForm

view = Blueprint("view", __name__)

OPTIONS = app.config['GAME_OPTIONS']


@view.route('/', methods=['GET', 'POST'])
def index():
    form = GameForm(request.form)

    if request.method == 'POST' and form.validate():
        # get user's choice
        mode = form.modes.data
        if mode == "3":
            width = form.width.data
            height = form.height.data
            mines = form.mines.data
        else:
            width = OPTIONS[int(mode)]['width']
            height = OPTIONS[int(mode)]['height']
            mines = OPTIONS[int(mode)]['mines']

        # generate game and save to database
        game = GameFactory.generate_new_game(width, height, mines)

        id = database.insert_game(game.to_json())

        return redirect(url_for('view.game', id=id))

    return render_template('/index.html', form=form)


@view.route('/game/<id>', methods=['GET'])
def game(id):
    game_data = database.get_game(id)
    if not game_data:
        abort(404)

    return render_template('game.html', id=id)


@view.route('/game_data/<id>', methods=['GET'])
def game_data(id):
    game_json = database.get_game(id)
    if not game_json:
        abort(404)

    game = Game(game_json['data'])

    return jsonify(game.to_json(is_view=True))


@view.route('/game_action', methods=['POST'])
def game_action():
    from datetime import datetime
    print("start")
    print(datetime.now())
    id = request.json['id']
    action = request.json['action']
    x = int(request.json['x'])
    y = int(request.json['y'])

    if not id or not action:
        abort(400)

    game_json = database.get_game(id)
    if not game_json:
        abort(404)

    game = Game(game_json['data'])

    if action == "click":
        game.open(x, y)
    if action == "right-click":
        print("flag")
        print(x)
        print(y)
        game.flag(x, y)
    if action == "double-click":
        game.double_open(x, y)

    database.update_game(id, game.to_json())
    print(datetime.now())
    return jsonify(game.to_json(is_view=True))
