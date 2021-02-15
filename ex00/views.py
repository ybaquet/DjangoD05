from django.http import HttpResponse
import psycopg2 as p

def init(request):
    command = """ \
(
    title character varying(64) NOT NULL,
    episode_nb integer NOT NULL,
    opening_crawl text,
    director character varying(32)  NOT NULL,
    producer character varying(128)  NOT NULL,
    release_date date NOT NULL,
    CONSTRAINT ex00_movies_pkey PRIMARY KEY (episode_nb),
    unique (episode_nb)
)
        """
    # connect to the PostgreSQL server
    conn = p.connect(host="localhost", database="djangoformation", user="djangouser", password="secret")
    try:
        cur = conn.cursor()
        # create table
        cur.execute(command)
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