from django.shortcuts import render
from django.http import HttpResponse
from django.db import *
import psycopg2 as p
from .models import Movies

def init(request):
    command = """ \
CREATE TABLE IF NOT EXISTS public.ex03_movies
(
    title character varying(64) NOT NULL,
    episode_nb integer NOT NULL,
    opening_crawl text,
    director character varying(32)  NOT NULL,
    producer character varying(128)  NOT NULL,
    release_date date NOT NULL,
    CONSTRAINT ex03_movies_pkey PRIMARY KEY (episode_nb),
    unique (episode_nb)
)
        """
    # connect to the PostgreSQL server
    conn = p.connect(host="localhost", database="djangoformation", user="djangouser", password="secret")
    try:
        cur = conn.cursor()
        # create table
        res = cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        return HttpResponse("OK")
    except (Exception, p.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
def populate(request):
    try:
        value_list = [      
             (1, 'The Phantom Menace', 'George Lucas', 'Rick McCallum', '1999-05-19'),
             (2, 'Attack of the Clones', 'George Lucas', 'Rick McCallum', '2002-05-16'),
             (3, 'Revenge of the Sith', 'George Lucas', 'Rick McCallum', '2005-05-19'),
             (4, 'A New Hope', 'George Lucas', 'Gary Kurtz, Rick McCallum', '1977-05-25'),
             (5, 'The Empire Strikes Back', 'Irvin Kershner', 'Gary Kutz, Rick McCallum', '1980-05-17'),
             (6, 'Return of the Jedi', 'Richard Marquand', 'Howard G. Kazanjian, George Lucas, Rick McCallum', '1983-05-25'),
             (7, 'The Force Awakens', 'J. J. Abrams', 'Kathleen Kennedy, J. J. Abrams, Bryan Burk', '2015-12-11'),
        ]
        ok = ''
        for record in value_list:
            try:
                old = Movies.objects.get(pk=record[0])
                ok = ok + 'Record (' + record[1] + '):' + "already exists" + "<br />"
            except (Movies.DoesNotExist) as error:
                m = Movies(episode_nb=record[0], title=record[1], director=record[2], producer=record[3], release_date=record[4] )
                m.save()
                ok = ok + ' OK<br />'
            except (Exception, p.DatabaseError) as error:
                ok = ok + 'Error on title(' + record[1] + '):' + str(error.pgcode) + ':' + str(error.pgerror) + "<br />"
        return HttpResponse(ok)
    except (Exception, p.DatabaseError) as error:
        print(error)
        return HttpResponse("ERROR")
            
def display(request):
        movies =  Movies.objects.all()
 #       print("movies: {}".format(movies))
        # print("longueur: {}".format(response.len))
        records = []
        for movie in movies:
            records.append((movie.episode_nb, movie.title, movie.opening_crawl, movie.director, movie.producer, movie.release_date ))
        return render(request, "display.html", {'records' : records })