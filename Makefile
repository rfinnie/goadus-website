FIND := find
PYTHON := python3

all:

lint:
	$(FIND) goadus -name '*.py' \
		-not -wholename 'goadus/migrations/*.py' -print0 | xargs \
		-0 $(PYTHON) -mflake8 --config=/dev/null \
		--ignore=C901,E203,E231,W503 --max-line-length=120

test: lint

black:
	$(PYTHON) -mblack --line-length=120 --exclude=migrations $(CURDIR)
