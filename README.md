<div>
  <h1 align="center">django-sslserver2</h1>
  <h4 align="center">
    Django package to support both HTTP and HTTPS as runserver command
  </h4>
</div>

## Usage

1. Install this package in you Django project

```bash
pip install django-sslserver2
```

2. Update Django's `settings.py`

```bash
INSTALLED_APPS = (...
    'sslserver2',
    ...
)
```

3. Execute you Django server:

```bash
python manage.py runsslserver2 --certificate cert.pem --key key.pem
```

## Development

### Requirements

- [Python v3.10.0](https://www.python.org/downloads/release/python-3100/)
- [Pipenv](https://pipenv.pypa.io)

### Update **requirements.txt**

As this project uses Pipenv on development, to keep compatibility with other
environments is recommended to generate the corresponding `requirements.txt`
file on every integration.

Run the following command to generate or overwrite the `requirements.txt` file:

```bash
pipenv lock -r > requirements.txt
```

## Releasing

1. Install `twine`

```bash
pip install twine
```

2. Build package distribution

```bash
python setup.py sdist bdist_wheel
```

3. Upload distribution

```bash
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
