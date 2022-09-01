from psycopg2 import sql
from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_show_count():
    return data_manager.execute_select('SELECT count(*) FROM shows;')


def get_shows_limited(order_by="rating", order="DESC", limit=0, offset=0):
    return data_manager.execute_select(
        sql.SQL("""
            SELECT
                shows.id,
                shows.title,
                EXTRACT(year FROM shows.year) AS year,
                shows.runtime,
                to_char(shows.rating::float, '999.9') AS rating,
                string_agg(genres.name, ', ' ORDER BY genres.name) AS genres,
                shows.trailer,
                shows.homepage
            FROM shows
                JOIN show_genres ON shows.id = show_genres.show_id
                JOIN genres ON show_genres.genre_id = genres.id
            GROUP BY shows.id
            ORDER BY
                CASE WHEN %(order)s = 'ASC' THEN {order_by} END ASC,
                CASE WHEN %(order)s = 'DESC' THEN {order_by} END DESC
            LIMIT %(limit)s
            OFFSET %(offset)s;
        """
        ).format(order_by=sql.Identifier(order_by)),
        {"order": order, "limit": limit, "offset": offset}
   )


def get_show_details_by_id(show_id):
    return data_manager.execute_select('''
    SELECT shows.id, title, year, overview, runtime, STRING_AGG(genres.name, ', ') genres, trunc(rating, 1) rating, trailer, homepage
    FROM shows
    LEFT JOIN show_genres ON shows.id=show_genres.show_id
    LEFT JOIN genres ON show_genres.genre_id=genres.id
    WHERE shows.id = %(show_id)s
    GROUP BY shows.id, title, year, overview, runtime, rating, trailer, homepage''',
    {"show_id": show_id})


def get_list_seasons(show_id):
    return data_manager.execute_select('''
    SELECT season_number, se.title, se.overview
    FROM seasons se
    LEFT JOIN shows s on se.show_id = s.id
    WHERE se.show_id = %(show_id)s''',
   {"show_id": show_id})


def get_top_3_actors(show_id):
    return data_manager.execute_select('''SELECT string_agg(x.name, ', ') as names
    FROM (
        SELECT a.name
        FROM actors a
        LEFT JOIN show_characters sc
            ON a.id = sc.actor_id
        LEFT JOIN shows s
            ON s.id = sc.show_id
        WHERE s.id = %(show_id)s
        GROUP BY sc.id, a.name
        ORDER BY sc.id
        LIMIT 3
    ) AS x;
    ''',
   {"show_id": show_id})


def get_actors():
    return data_manager.execute_select("""
    SELECT a.name, count(s.id) FROM actors a
        INNER JOIN show_characters sc on a.id = sc.actor_id
        INNER JOIN seasons s on sc.show_id = s.show_id
    WHERE name ilike '%a'
    GROUP BY a.name
    HAVING count(s.id) <  10
    LIMIT 5;""")


# def get_years():
#     return data_manager.execute_select("""SELECT  EXTRACT(year FROM a.birthday) AS year FROM actors a""")


def get_seasons():
    return data_manager.execute_select("""
    select seasons.id, seasons.title, seasons.season_number
    from seasons
        inner join episodes e on seasons.id = e.season_id
    where seasons.title ilike 'a%'
    group by seasons.id, seasons.title, seasons.season_number
    having count(e.title) > 10;""")
    

def get_episodes(title):
    return data_manager.execute_select("""
    select episodes.title 
    from episodes
    inner join seasons s on episodes.season_id = s.id
    where s.title = %(title)s""", {"title": title})


def get_show_actors():
    return data_manager.execute_select("""
    SELECT a.id, a.name FROM actors a
        INNER JOIN show_characters sc on a.id = sc.actor_id
        INNER JOIN shows on sc.show_id = shows.id
    GROUP BY 1, 2
    HAVING count(shows.id) >= 6;""")


def get_shows6(actor):
    return data_manager.execute_select("""
    SELECT DISTINCT s.title FROM shows s
        INNER JOIN show_characters sc on s.id = sc.show_id
        INNER JOIN actors a on sc.actor_id = a.id
                        INNER JOIN show_genres sg on s.id = sg.show_id
                        INNER JOIN genres g on sg.genre_id = g.id
        WHERE g.name = 'Drama' AND a.id = %(actor)s;""", {'actor': actor})
