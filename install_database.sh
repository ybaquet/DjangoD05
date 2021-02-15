create database djangoformation;
CREATE USER djangouser WITH PASSWORD 'secret';
GRANT ALL PRIVILEGES ON DATABASE "djangoformation" to djangouser;



conn = p.connect(host="localhost", database="djangoformation", user="djangouser", password="secret")