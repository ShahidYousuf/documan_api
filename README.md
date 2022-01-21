# documan_api
A simple document management REST based API for collaboratively interacting with documents.

### Tech Stack

+ [Python3.10.1](https://www.python.org/)
+ [Django](https://www.djangoproject.com/)
+ [Django Rest Framework](https://www.django-rest-framework.org/)
+ [SQLite](https://www.sqlite.org/index.html)

> ℹ️: **For Demo and Test Purposes**: Please use .txt file uploads. Once interacted with, these files are appended with action log text lines.

### Steps to run the application on your local machine
```bash
virtualenv <name_python_env> -p python3.10
```

```bash
cd <some_directory_on_your_computer>
```

```bash
git clone https://github.com/ShahidYousuf/documan_api.git
```

```bash
cd documan_api
```

```bash
source <path_to_your_env>/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```
check the application running on [localhost:8000](http://localhost:8000).

#### Contributions are welcome. Just create your own branch and send a pull request. Happy coding!
