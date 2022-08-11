from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated_shows():
    return data_manager.execute_select('''SELECT shows.id, title, year, overview, runtime, STRING_AGG(genres.name, ', ') genres, trunc(rating, 1) rating, trailer, homepage
                      FROM shows
                      LEFT JOIN show_genres ON shows.id=show_genres.show_id
                      LEFT JOIN genres ON show_genres.genre_id=genres.id
                      GROUP BY shows.id, title, year, overview, runtime, rating, trailer, homepage
                      ORDER BY rating DESC
                      LIMIT 15''')


def get_show_details_by_id(show_id):
    return data_manager.execute_select('''SELECT shows.id, title, year, overview, runtime, STRING_AGG(genres.name, ', ') genres, trunc(rating, 1) rating, trailer, homepage
                      FROM shows
                      LEFT JOIN show_genres ON shows.id=show_genres.show_id
                      LEFT JOIN genres ON show_genres.genre_id=genres.id
                      WHERE shows.id = %(show_id)s
                      GROUP BY shows.id, title, year, overview, runtime, rating, trailer, homepage''',
                       {"show_id": show_id})


def get_list_seasons(show_id):
    return data_manager.execute_select('''SELECT season_number, se.title, se.overview
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
