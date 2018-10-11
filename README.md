# Simple REST API


## Task

Build simple REST API - a basic movie database interacting with external API.
Full specification of endpoints:

**POST /movies:**

- [ ] Request body should contain only movie title, and its presence should be validated.
- [X] Based on passed title, other movie details should be fetched from http://www.omdbapi.com/
      (or other similar, public movie database) - and saved to application database.
- [ ] Request response should include full movie object, along with all data fetched from external API.

**GET /movies:**

- [X] Should fetch list of all movies already present in application database.
- [X] Additional filtering, sorting is fully optional - but some implementation is a bonus.

**POST /comments:**

- [X] Request body should contain ID of movie already present in database, and comment text body.
- [X] Comment should be saved to application database and returned in request response.

**GET /comments:**

- [X] Should fetch list of all comments present in application database.
- [X] Should allow filtering comments by associated movie, by passing its ID.

**GET /top:**

- [ ] Should return top movies already present in the database ranking
      based on a number of comments added to the movie (as in the example) in the specified
      date range. The response should include the ID of the movie, position in rank and total
      number of comments (in the specified date range).
- [X] Movies with the same number of comments should have the same position in the ranking.
- [ ] Should require specifying a date range for which statistics should be generated.
Example response:

```json
[
    {
        "movie_id": 2,
        "total_comments": 4,
        "rank": 1
    },
    {
        "movie_id": 3,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 4,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 1,
        "total_comments": 0,
        "rank": 3
    }
]
```

**Rules & hints**

The goal is to implement REST API in Django, however feel free to use any third-party libraries and database
of your choice, but please share your reasoning behind choosing them.
- [ ] At least basic tests of endpoints and their functionality are obligatory.
      Their exact scope and form is left up to you.
- [ ] The application's code should be kept in a public repository so that we can read it, pull it and build
      it ourselves. Remember to include README file or at least basic notes on application requirements
      and setup - we should be able to easily and quickly get it running.
- [ ] Written application must be hosted and publicly available for online - example Heroku.

## Install
```bash
git clone repository
(venv) pip install -r requirements.txt
cp credentials.conf.template credentials.conf
# provide valid OMDB API key in credentials.conf
python manage.py migrate
# optionally python manage.py createsuperuser
```

## Test
Just run
```bash
cd src/pmdb
pytest
```
from command line

## Run
For development purposes:
```bash
(venv) python manage.py runserver
```

# Other

```
python manage.py show_urls
```
