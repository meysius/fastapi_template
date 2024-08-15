poetry run alembic upgrade head
poetry run alembic downgrade -1

Initialize alembic with async template:
alembic init -t async alembic

alembic revision --autogenerate -m "Adding user model"
alembic current --verbose


poetry run python console.py