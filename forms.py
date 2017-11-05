from wtforms import form, fields, validators, ValidationError
from wtforms.widgets.html5 import NumberInput
from flask import current_app as app


class GameForm(form.Form):
    OPTIONS = app.config['GAME_OPTIONS']
    MINIMUM = app.config['GAME_MINIMUM']
    MAXIMUM = app.config['GAME_MAXIMUM']

    modes = fields.RadioField(
        label='Modes',
        choices=[
            ("0", str(OPTIONS[0]['width']) + ' x ' + str(OPTIONS[0]['height'])),
            ("1", str(OPTIONS[1]['width']) + ' x ' + str(OPTIONS[1]['height'])),
            ("2", str(OPTIONS[2]['width']) + ' x ' + str(OPTIONS[2]['height'])),
            ("3", 'Custom')
        ],
        default='0',
        validators=[validators.Required()]
    )

    width = fields.IntegerField(
        label='Width',
        default=MINIMUM['width'],
        validators=[validators.NumberRange(min=MINIMUM['width'], max=MAXIMUM['width'])],
        widget=NumberInput(min=MINIMUM['width'], max=MAXIMUM['width'])
    )

    height = fields.IntegerField(
        label='Height',
        default=MINIMUM['height'],
        validators=[validators.NumberRange(min=MINIMUM['height'], max=MAXIMUM['height'])],
        widget=NumberInput(min=MINIMUM['height'], max=MAXIMUM['height'])
    )

    mines = fields.IntegerField(
        label='Mines',
        default=MINIMUM['mines'],
        validators=[validators.NumberRange(min=MINIMUM['mines'], max=MAXIMUM['mines'])],
        widget=NumberInput(min=MINIMUM['mines'], max=MAXIMUM['mines'])
    )

    start = fields.SubmitField(label='New Game')
