# Bike Shop Backend

You can develop on the backend without Docker.

Create a virtual environment with (you can also use it in Visual Studio):

```sh
cd backend
python3 -m venv .venv
```

Then activate it with:

```sh
source .venv/bin/activate
```

You can install dependencies with:

```sh
pip install -r requirements.txt
```

Make sure to copy `.env.example` to `.env`, then you can run the server with (this will reload the server when there are changes in the code).

First, run the migrations for the database:

```sh
alembic upgrade head
```

Then start the uvicorn server:

```sh
python3 asgi.py
```

To run the tests manually, just run:

```sh
pytest
```

Use `pytest tests/api/test_utils.py` to run a specific suite of tests or `pytest tests/api/test_services.py::test_create_product_success`.

You can run flake and black for code formatting manually, or set your editor reformat on Save.

```sh
black .
flake8 . --exclude venv,.venv
```
