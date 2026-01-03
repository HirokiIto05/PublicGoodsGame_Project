SESSION_CONFIGS = [
    dict(
        name='dictator_app',
        display_name="Simple Dictator Game",
        app_sequence=['dictator_app'],
        num_demo_participants=1,
    ),
    dict(
        name='multiple_app',
        display_name="Multiple App",
        app_sequence=['multiple_app'],
        num_demo_participants=1,
    ),
    dict(
        name='pgg_base',
        display_name="Public Goods Game Base",
        app_sequence=['pgg_base'],
        num_demo_participants=2,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

LANGUAGE_CODE = 'en'


LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

INSTALLED_APPS = ['otree']

SECRET_KEY = 'replace-me'
DEBUG = True