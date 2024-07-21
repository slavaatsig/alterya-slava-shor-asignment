# Slava Shor Alterya Assignment

A Poetry src structured Python project.
Prerequisites:

* Python 3.12
* Latest Poetry
* An `.env` file at root of the project with API key `COVALENTHQ_API_KEY=cqt_wFb*********wqB` or exported as OS env
  variable (also for unit tests)

Please note, it is advisable to configure Poetry to create virtual
environments inside the project:

```shell
python3.12 -m poetry config virtualenvs.create true
```

To install project in local virtual environment:

```shell
python3.12 -m poetry install
```

To run the REST API service

```shell
python3.12 -m poetry run uvicorn alterya.service:app --host 127.0.0.1 --port 8000 --reload
```

It executes REST API app exactly as same as the `main.py` entry point does, but explicitly from CLI.

NOTE: It listens on local host only. If you wish to reach from outside your local host then set listen on `0.0.0.0`.