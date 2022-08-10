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


# def get_show_by_id(show_id):
#     return data_manager.execute_select('''SELECT * FROM shows WHERE id = %(show_id)s''',
#                                        {"show_id": show_id})
