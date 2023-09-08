python = python3
pip = pip3


test_fixtures = */fixtures/*.test.json

backend-server-start:
	$(python) -u manage.py runserver localhost:8050
	tail -f django-server.log 

install:
	$(pip) install -r requirements.txt 


testing:
	$(python) manage.py loaddata $(test_fixtures)


setup:
	$(python) manage.py makemigrations && $(python) manage.py migrate

backend-db-refresh:
	rm -rf db.sqlite3 2>/dev/null
	find . -type d -name migrations | xargs -I {} find {} -type f -name "*.py" | grep -v '__init__.py' | grep -v 'postgres-dev' | xargs rm -f 2>/dev/null


clear-cache:
	find . -name "__pycache__" | xargs rm -r

clear-migraions:
	find . -name "*initial.py" | xargs rm -r

shell-plus:
	$(python) manage.py shell_plus --ipython

broker-start:
	sudo systemctl  start docker
	sudo docker run --rm -it -p 15672:15672 -p 5672:5672 rabbitmq:3-management





clear-cache:
	find . -name "__pycache__" | xargs rm -r