# Full Stack Capstone Project

## Casting Agency

As part of Casting Agency  system, we are building set of services that can enable the application users to 

1) View all the actors and movies from the database
2) Add a new actor, movie and add actors to a movie and vice versa.
3) Modify the details of movies and actors
4) Delete movies and actors.

## API Behavior and Roles

This application consists of 3 roles
1) `Casting Assistant` - A casting assistant can view the actor and movie records. A Casting agent can access `GET /actors` and `GET /movies` endpoint
2) `Casting Director` - All permisions that a casting assistant has and additionally add and delete actors and also modify movies or actors. A Casting agent can access `GET /actors`, `GET /movies`, `POST /actors`, `PATCH /actor` , `DELETE /actor`, `PATCH /movie` endpoint
3) `Executive Producer` - All permissions that a casting director has and additionally add or delete movies `POST /movies` , `DELETE /movie`.

## Error Handling

Different Types of error from the application

- 400 Bad Request
- 404 Resource Not Found
- 401 Unauthorized
- 500 Internal Server Error

## End Points

### 1. GET /actors
- get the list of actors on the system
- this API requires get:actors-movies permission to access

`Response Sample`

```
{
  "actors": [
    {
      "age": 27,
      "first_name": "Albon",
      "gender": "Male",
      "id": 31,
      "last_name": "Alex"
    }
  ],
  "success": true
}
```

### 2. GET /movies
- get the list of movies on the system
- this API requires get:actors-movies permission to access

`Response Sample`

```
{
  "movies": [
    {
      "actors": [
        {
          "age": 27,
          "first_name": "Albon",
          "gender": "Male",
          "id": 31,
          "last_name": "Alex"
        }
      ],
      "id": 23,
      "release_date": "Fri, 21 Aug 2020 00:51:07 GMT",
      "title": "A new movie4"
    }
  ],
  "success": true
}
```

### 3. POST /actors
- add an actor to the system
- generate actor_id as a response
- requires a permission add: actors

`Request Sample`

```
{
    "first_name": "Arjun",
    "last_name":"qwqwqw",
    "age": 21
}
```
`Response Sample`

```
{
  "id": 32,
  "success": true
}
```

### 4. POST /movies
- add an movie and map corresponding actors to the system
- generate movie id as a response
- requires a permission add: movies

`Request Sample`

```
{
    "title": " A new movie4",
    "release_date": "2020-08-20 00:51:07",
    "actors_id": [1]
}
```
`Response Sample`

```
{
  "id": 32,
  "success": true
}
```

### 5. Delete /actor/<id>
- Delete an actor from the database if the actor id is valid
- requires a delete: actors permission level

`Response Sample`

```
{
  "deleted_actor_id": "6",
  "success": true
}
```

### 6. Delete /movie/<id>
- Delete a movie from the database if the movie id is valid
- requires a delete: movies permission level

`Response Sample`

```
{
  "deleted_movie_id": "6",
  "success": true
}
```
### 7. Patch /actor/<id>
- Update an actor detail from the database if the actor id is valid
- requires a mdify: actors permission level

`Request Sample`

```
{
  "last_name": "Albon"
}
```


`Response Sample`

```
{
  "updated_actor_id": "6",
  "success": true
}
```

### 8. Patch /movie/<id>
- Update an movie detail from the database if the actor id is valid
- requires a mdify: movies permission level

`Request Sample`

```
{
  "title": "A new movie 5"
}
```


`Response Sample`

```
{
  "updated_movie_id": "6",
  "success": true
}
```

## Installation and Dependency

1. Install all the python and pip dependencies for a flask app
2. Following dependents needs to be installed

```
FLASK
SQLALCHEMY
FLASK MIGRATE
FLASK CORS
```
To install all the requirements, run the following command

```
pip install -r requirements.txt
```

## Run locally

To run the app locally, go to the project directory and execute below commands.

```
export FLASK_APP = flaskr
export FLASK_ENV = development
flask run
```
`Note: if you are running on a windows environment use SET instead of EXPORT above, example: set FLASK_APP = flaskr`

## Test Locally

There are two ways to test this application locally.
### 1. POSTMAN
- Using end point details from can be run in postman. To install postman click [here](https://www.postman.com/downloads/)
- The Bearer token is available to be used inside `config.py`

### 2. Python Unit test
- cd project directory in terminal
- Run `python test_api.py` or `python3 test_api.py` if you are running python3