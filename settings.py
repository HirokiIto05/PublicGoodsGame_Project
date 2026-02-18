SESSION_CONFIGS = [
    dict(
        name='pgg_sym_peer',
        display_name='PGG diff punishment - symmetric, peer only',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=0,
        punishment_system=1,  # 0:none, 1:peer, 3:central
    ),
    dict(
        name='pgg_asym_peer',
        display_name='PGG diff punishment - asymmetric, peer only',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=1,
        punishment_system=1,
    ),
    dict(
        name='pgg_sym_democratic',
        display_name='PGG diff punishment - symmetric, democratic',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=0,
        punishment_system=2,  # 0:none, 1:peer, 3:central
    ),
    dict(
        name='pgg_40_40_20_20',
        app_sequence=['pgg_diff_punishment'],
        num_demo_participants=4,
        punishment_system=1,
        endowment_profile='asym_40_40_20_20',
    ),
    dict(
        name='pgg_80_40_20_20',
        app_sequence=['pgg_diff_punishment'],
        num_demo_participants=4,
        punishment_system=1,
        endowment_profile='asym_80_40_20_20',
    )

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