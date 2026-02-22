SESSION_CONFIGS = [
    dict(
        name='sym_complete',
        display_name='symmetric, perfect info (peer→democratic)',
        num_demo_participants=4,
        app_sequence=['pgg_asymmetric_punishment'],
        asymmetry=0,
        punishment_info_mode='full',
    ),
    dict(
        name='sym_incomplete',
        display_name='symmetric, imperfect info (peer→democratic)',
        num_demo_participants=4,
        app_sequence=['pgg_asymmetric_punishment'],
        asymmetry=0,
        punishment_info_mode='incomplete',
    ),
    dict(
        name='asym_small_complete',
        display_name='asymmetric(small), perfect info (peer→democratic)',
        num_demo_participants=4,
        app_sequence=['pgg_asymmetric_punishment'],
        asymmetry=1,
        punishment_info_mode='full',
    ),
    dict(
        name='asym_small_incomplete',
        display_name='asymmetric(small), imperfect info (peer→democratic)',
        num_demo_participants=4,
        app_sequence=['pgg_asymmetric_punishment'],
        asymmetry=1,
        punishment_info_mode='incomplete',
    ),
    dict(
        name='asym_large_complete',
        display_name='asymmetric(large), perfect info (peer→democratic)',
        num_demo_participants=4,
        app_sequence=['pgg_asymmetric_punishment'],
        asymmetry=2,
        punishment_info_mode='full',
    ),
    dict(
        name='asym_large_incomplete',
        display_name='asymmetric(large), imperfect info (peer→democratic)',
        num_demo_participants=4,
        app_sequence=['pgg_asymmetric_punishment'],
        asymmetry=2,
        punishment_info_mode='incomplete',
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