# djazz
Djazz is helper library for Django framework

#### How to install
1. via pip: `pip install git+https://github.com/akoikelov/djazz`
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

#### Backup

For backup of database and media files, there is a command:

`python manage.py backup [--save] [--load] [--include-media] [--replace]`

* --save: option for saving backup
* --load: option for loading latest backup
* --include-media: also backup media files
* --replace: Delete old backups and replace them with a new backup

We store backups at Dropbox.
Add `DROPBOX_ACCESS_TOKEN` param to settings.py, containing dropbox access token