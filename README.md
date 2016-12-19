# djazz
Djazz is helper library for Django framework

#### How to install
1. via pip: `pip install akoikelov.djazz`
or
2. download repository: https://github.com/akoikelov/djazz and run script `./install.sh`

#### How to use it

1. Add `akoikelov.djazz` to INSTALLED_APPS in settings.py:
`INSTALLED_APPS = [
    ...
    'tastypie',
    'akoikelov.djazz'
]`

There are several commands inside:
- `python manage.py generate_model [app_name] [model_name]`
- `python manage.py generate_admin [app_name]`
- `python manage.py generate_api [app_name] [main_app_name]` (requires tastypie library)