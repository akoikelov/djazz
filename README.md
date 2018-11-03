# djazz
Djazz is helper library for Django framework

## Installation
1. via pip: `pip install git+https://github.com/akoikelov/djazz`
or
2. download repository: https://github.com/akoikelov/djazz and run script `./install.sh`

## Configuration

Add `akoikelov.djazz` to INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    'tastypie',
    'akoikelov.djazz'
]
```

### Code generators

There are several commands inside:
- `python manage.py gen_model [app_name] [model_name]`
- `python manage.py gen_admin [app_name]`

### Backup tool

For backup of database and media files, there is a command:

- `python manage.py backup [-s] [-m] [-r]`
- `python manage.py backup [-l]`

* -s: option for saving backup
* -l: option for loading latest backup
* -m: also backup media files
* -r: Delete old backups and replace them with a new backup

We store backups at Dropbox.
Add `DROPBOX_ACCESS_TOKEN` param to settings.py, containing dropbox access token