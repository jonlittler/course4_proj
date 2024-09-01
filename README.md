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
