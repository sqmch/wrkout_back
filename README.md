# wrkout (WIP) - a web based fitness app for creating, performing and tracking workouts

## Built with

- Python (FastAPI, postgres with SQLAlchemy)
- Vue.js (Quasar)

### Demo: https://wrkout1.netlify.app/
Frontend hosted on Netlify, backend hosted on Heroku, using Heroku Postgres.

## About the project

wrkout aims to be an useful workout companion app, allowing the user to create workout routines and perform them set by set, all while tracking the user's progress over time and providing useful visual overviews of the data gathered from workout routines.


## How to run locally

Use poetry for creating a virtual environment and installing dependencies:
```
poetry shell
poetry install
```


Run FastAPI:
```python
uvicorn wrkout2_back.main:app --reload
```
