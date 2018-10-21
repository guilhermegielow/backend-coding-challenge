# Unbabel Backend Challenge

Hey :smile:

I built a simple app using python 2.7 with Flask with connection with Postgres by SQLAlchemy and the interface is HTML with bootstrap.
In my tests I used Unittest.

## How it works?

The input text is submitted to Unbabel API in sandbox and it will go to the table and save the translation in the table "translations" of the postgres.
In the next translation the app will ask to API about the queue translations and it will update the table and 
a row in the table "translations" of the postgres.

## Software Version

* Python 2.7.15

* Postgres 9.6.6

* Flask 1.0.2

#### Notes
* In the future I could use ReactJs or JQuery to improve the app's functionality. 

#### Resources
* Unbabel's API: http://developers.unbabel.com/

