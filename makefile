install:
	rm -rf vendors/amazonProductApiCrawler/
	git clone git@github.com:johnHackworth/amazonProductApiCrawler.git ./vendors/amazonProductApiCrawler/
	rm -rf vendors/lastfmCrawler/
	git clone git@github.com:johnHackworth/lastfmCrawler.git ./vendors/lastfmCrawler/
	sudo pip install django
	sudo pip install pytz
	sudo pip install bottlenose
	sudo pip install django-piston
	sudo apt-get install mysql-server
	sudo apt-get install python-mysqldb
	mysql -u root < install.sql
	./manage.py syncdb

server:
	./manage.py runserver 0.0.0.0:8000
