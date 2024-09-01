# course4_proj

OMDB project in Course 4 of Advanced Django specialization

This is the starting point of the project. It is the equivalent of running `django-admin startproject course4_proj` in the terminal.

### OMDB

1. Go to the course4_proj repo. This repo contains the starting point for this project.
2. Click on the “Fork” button in the top-right corner.
3. Click the green “Code” button.
4. Copy the SSH information.

https://github.com/codio-templates/course4_proj

```bash
git clone git@github.com:jonlittler/course4_proj.git
```

The Open Movie Database is a free REST web service that can be queried to get information about movies. To follow along with these examples, and complete modules 3 and 4, you’ll need an API key. One can be obtained free from:-

https://www.omdbapi.com/apikey.aspx

```python
import os
import requests

params = {"apikey": os.environ["DJANGO_OMDB_KEY"], "t": "star wars"}
resp = requests.get("https://www.omdbapi.com/", params=params)

print(resp.json())
```

Next we are going to define a class that acts as an intermediary/transformer between the JSON dictionary returned from OMDb and raw Python data. It’s responsible for:

- Validating and transforming the movie’s runtime.
- Converting the movie’s year into and int.
- Checking if keys are set and raising exceptions if trying to access detail keys on non-detail response.
- Splitting the genre into a list.

```python
# data is a dictionary from the API
data = {"Title": "My Great Movie", "Year": "1991"}
movie = OmdbMovie(data)
movie.title     # 'My Great Movie'
movie.year      # 1991  # notice that this is an integer
movie.plot      # AttributeError: Plot is not in data
```

### Running Python Management Commands

Create movie_search.py in movies/management/commands and run with the following command.

```bash
python3 manage.py movie_search django unchained
python3 manage.py movie_fill tt1853728
python3 manage.py shell
```

```python
from movies.models import Movie, Genre
movies = Movie.objects.all()
for movie in movies:
    print(movie.title, movie.year)
```

### Important Takeaway Points

- API keys can be fetched from Django settings. Consider using a SecretValue field to retrieve them from the environment, similar to the SECRET_KEY setting.
- Your REST client should have a single method that’s called to make requests. This means you have only one place to implement authentication and HTTP error handling, rather than littering your code with them.
- REST clients should not be directly tied to Django. Allow your REST client to be instantiated without knowing about any Django settings.
- The client should also not be responsible for inserting any data into the Django database.
- It is OK to create a helper class or function that will instantiate the REST client from the Django settings.
- Don’t return the response body directly from your client (the decoded JSON response dictionary, for example). Instead, use a transformation function or class to turn it into a standard format. This means if the API starts returning different data you only have one place to update the parser.
- Check what data comes back for a list or detail response. Your models may need to keep track if they are a full response or not. This could be just a flag, or a datetime if the model data needs to be refreshed periodically.
- Consider some protection against users causing repeated API calls for the same data.
- (This point is not REST API specific:) Having helper functions outside of your view code means you can use the functionality in management commands as well, without having to write duplicate code.

## PyGithub

```bash
pip3 install PyGithub
python3 manage.py startapp gh
```

Generate GiyHub Token https://github.com/settings/tokens/new

#### Testing

```bash
python3 manage.py test books.tests_1
```

## Module 2

Welcome to Week 2 of the Advanced Django: External APIs and Task Queuing course. These assignments cover working with asynchronous tasks using Celery and Django Signals. The module ends with graded coding exercises.

Learning Objectives

- Explain the benefits of Celery
- Differentiate between Celery and Redis
- Register a Celery task
- Fetch a completed task
- View task results in the Admin GUI
- Define a signal and explain its benefits
- Create a receiver with a method and a decorator
- Prevent the reception of duplicate signals
- Create an asynchronous signal
- Create your own signal
- Define a task signature
- Create a periodic task
- Differentiate between interval, crontab, solar, and clocked schedules
- Explain how Celery Beat works
- Schedule tasks that run on an interval or on a specified date/time

### Celery & Redis

```bash
# download codebase
git clone git@github.com:jonlittler/course4_proj.git

# install redis / celery
sudo apt install -y redis
redis-cli ping              # PONG
pip3 install celery django-celery-results redis
python3 manage.py migrate

# start celery worker
celery -A course4_proj worker -l DEBUG
```

Where:

- A is the application argument, in this case we want to import it from the course4_proj module.
  worker is the command to run, which means start a worker instance
- l sets the log level, we set it to INFO. You could also use DEBUG, WARN, ERROR, etc

It’s a library that is used to run tasks outside of the main web process. At a high level, tasks are put into a queue (the time to write the task to the queue is fast).

The main webserver process can then continue, and return a response to the client. Meanwhile, a broker reads from the queue and passes the task on to worker(s) that process/execute the task and puts the results back into a queue or database.

https://docs.celeryq.dev/en/stable/userguide/configuration.html

### \_\_init\_\_.py

https://docs.python.org/3/reference/import.html#regular-packages

Python defines two types of packages, regular packages and namespace packages. Regular packages are traditional packages as they existed in Python 3.2 and earlier. A regular package is typically implemented as a directory containing an \_\_init\_\_.py file.

When a regular package is imported, this \_\_init**.py file is implicitly executed, and the objects it defines are bound to names in the package’s namespace. The \_\_init**.py file can contain the same Python code that any other module can contain, and Python will add some additional attributes to the module when it is imported.

```python
# regular way
value = my_long_running_function("arg1", 2)
print(value)

# celery way
res = my_long_running_function.delay("arg1", 2)
value = res.get()
print(value)

# async
from course4_proj.celery import app

res = my_long_running_function.delay("arg1", 2)
task_id = res.id

res = app.AsyncResult(task_id)  # load the AsyncResult
value = res.get()               # get the value
```

> NOTE: redirect doesn't work in Codio BoxURL

Search\
https://sodamystery-mercyplace-8000.codio.io/search/?search_term=star+wars

Search Wait\
https://sodamystery-mercyplace-8000.codio.io/search-wait/6e3139b3-7299-4b6f-bb9f-bd1b900ced1f/?search_term=star+wars

Search Results\
https://sodamystery-mercyplace-8000.codio.io/search-results/?search_term=star+wars

### Django Signals

https://docs.djangoproject.com/en/3.2/ref/signals/

```bash
# download codebase
git clone git@github.com:jonlittler/course4_proj.git
```

Django Signals are used to listen to events throughout the lifetime of a Django application executing (whether with a request, using manage.py, or otherwise).

This allows a Django project to easily run code in response to events even in third-party apps and can be easier than trying to get similar results with other techniques, like subclassing.

Most Common:

- `django.db.models.signals.pre_save` / `django.db.models.signals.post_save:` Sent before/after a model’s save() method is called.
- `django.db.models.signals.pre_delete` / `django.db.models.signals.post_delete`: Sent before/after a model or queryset’s delete() method is called.
- `django.db.models.signals.m2m_changed`: Sent when a ManyToManyField on a model is changed.
- `django.core.signals.request_started` / `django.core.signals.request_finished`: Sent before/after a Django request is handled.

> The **`# noqa`** at the end of the import line instructs linters to ignore this line when checking the code format. Without it, we could get an error or warning that the import is not used.

Testing using management commands

```bash
python3 manage.py movie_search "finding nemo"
```
