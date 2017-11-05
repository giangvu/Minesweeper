from flask import Blueprint, request, render_template, redirect, url_for, current_app as app, jsonify, abort
from db_connector import DatabaseConnector as database
from game_factory import GameFactory
from game import Game
from forms import GameForm
from extensions import socket
from flask_socketio import emit, join_room, leave_room

view = Blueprint("view", __name__)

OPTIONS = app.config['GAME_OPTIONS']


@socket.on('join')
def join(id):
    join_room(id)

    game_json = database.get_game(id)
    if not game_json:
        abort(404)

    game = Game(game_json['data'])

    emit('game-data', game.to_json(is_view=True), room=id)


@socket.on('action')
def action(message):
    id = message['id']
    action = message['action']
    x = int(message['x'])
    y = int(message['y'])

    game_json = database.get_game(id)
    if not game_json:
        abort(404)

    game = Game(game_json['data'])

    if action == "click":
        game.open(x, y)
    if action == "right-click":
        game.flag(x, y)
    if action == "double-click":
        game.double_open(x, y)

    database.update_game(id, game.to_json())

    emit('game-data', game.to_json(is_view=True), room=id)


@socket.on('leave')
def left(id):
    leave_room(id)
    # emit('status', {'msg': session.get('name') + ' has left the room.'}, room=game_id)


@socket.on('disconnect')
def disconnect():
    print(request.sid)
    print(request.url)
    print('Client disconnected')


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

