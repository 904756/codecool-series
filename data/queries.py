from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_most_rated_shows():
    return data_manager.execute_select('''SELECT title, year, runtime, STRING_AGG(genres.name, ',') genres , trunc(rating, 1) rating, trailer, homepage
                      FROM shows
                      LEFT JOIN show_genres ON shows.id=show_genres.show_id
                      LEFT JOIN genres ON show_genres.genre_id=genres.id
                      GROUP BY title, year, runtime, rating, trailer, homepage
                      ORDER BY rating DESC
                      LIMIT 15''')
