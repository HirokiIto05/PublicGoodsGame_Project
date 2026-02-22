SESSION_CONFIGS = [
    dict(
        name='sym_peer_complete',
        display_name='symmetric, peer, perfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=0,
        punishment_system=1,  # 1:peer, 2:democratic
        punishment_info_mode='full'
    ),
    dict(
        name='sym_peer_incomplete',
        display_name='symmetric, peer, imperfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=0,
        punishment_system=1,  # 1:peer, 2:democratic
        punishment_info_mode='incomplete'
    ),
    dict(
        name='sym_democratic_complete',
        display_name='symmetric, democratic, perfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=0,
        punishment_system=2,  # 1:peer, 2:democratic
        punishment_info_mode='full'
    ),
    dict(
        name='sym_democratic_incomplete',
        display_name='symmetric, democratic, imperfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=0,
        punishment_system=2,  # 1:peer, 2:democratic
        punishment_info_mode='incomplete'
    ),
    dict(
        name='asym_small_peer_complete',
        display_name='asymmetric(small), peer, perfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=1,
        punishment_system=1,
        punishment_info_mode='full'
    ),
    dict(
        name='asym_small_peer_incomplete',
        display_name='asymmetric(small), peer, imperfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=1,
        punishment_system=1,
        punishment_info_mode='incomplete'
    ),
    dict(
        name='asym_small_democratic_complete',
        display_name='asymmetric(small), democratic, perfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=1,
        punishment_system=2,
        punishment_info_mode='full'
    ),
    dict(
        name='asym_small_democratic_incomplete',
        display_name='asymmetric(small), democratic, imperfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=1,
        punishment_system=2,
        punishment_info_mode='incomplete'
    ),
    dict(
        name='asym_large_peer_complete',
        display_name='asymmetric(large), peer, perfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=2,
        punishment_system=1,
        punishment_info_mode='full'
    ),
    dict(
        name='asym_large_peer_incomplete',
        display_name='asymmetric(large), peer, imperfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=2,
        punishment_system=1,
        punishment_info_mode='incomplete'
    ),
    dict(
        name='asym_large_democratic_complete',
        display_name='asymmetric(large), democratic, perfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=2,
        punishment_system=2,  # 1:peer, 2:democratic
        punishment_info_mode='full'
    ),
    dict(
        name='asym_large_democratic_incomplete',
        display_name='asymmetric(large), democratic, imperfect',
        num_demo_participants=4,
        app_sequence=['pgg_diff_punishment'],
        asymmetry=2,
        punishment_system=2,  # 1:peer, 2:democratic
        punishment_info_mode='incomplete'
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
ALLOWED_HOSTS = ['*']