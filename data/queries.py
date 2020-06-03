import data_manager, bcrypt

def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


@data_manager.connection_handler
def get_shows_direction(cursor):
    cursor.execute('''SELECT shows.id, title, year, runtime, ROUND(rating, 2) AS rating, trailer, homepage
                    FROM shows
                    ORDER BY rating DESC
                    LIMIT 15''')
    return cursor.fetchall()


@data_manager.connection_handler
def resorting(cursor, pagination, sort_by_elem, direction):
    cursor.execute(f'''SELECT shows.id, title, year, runtime, ROUND(rating, 2) AS rating, trailer, homepage
                    FROM shows
                    ORDER BY {sort_by_elem} {direction}
                    LIMIT 15 OFFSET {pagination}''')
    return cursor.fetchall()


@data_manager.connection_handler
def get_genre(cursor):
    cursor.execute('''SELECT name 
                    FROM genres
                    INNER JOIN show_genres ON genres.id = show_genres.genre_id
                    INNER JOIN shows ON shows.id = show_genres.show_id
                    LIMIT 15''')
    return cursor.fetchall()


@data_manager.connection_handler
def genre_sort(cursor, direction):
    cursor.execute(f'''SELECT name 
                    FROM genres
                    INNER JOIN show_genres ON genres.id = show_genres.genre_id
                    INNER JOIN shows ON shows.id = show_genres.show_id
                    ORDER BY name {direction}
                    LIMIT 15''')
    return cursor.fetchall()


@data_manager.connection_handler
def get_show(cursor, show_id):
    cursor.execute(f'''SELECT id, title, year, overview, trailer, runtime
                    FROM shows
                    WHERE shows.id = {show_id}''')
    return cursor.fetchone()


@data_manager.connection_handler
def get_actors(cursor, show_id):
    cursor.execute(f'''SELECT name
                      FROM actors
                      INNER JOIN show_characters ON actors.id = show_characters.actor_id
                       WHERE show_id = {show_id}''')
    return cursor.fetchall()


@data_manager.connection_handler
def get_seasons(cursor, show_id):
    cursor.execute(f'''SELECT season_number, title, overview
                      FROM seasons
                      WHERE show_id = {show_id}''')
    return cursor.fetchall()


@data_manager.connection_handler
def get_page(cursor, pagination):
    cursor.execute(f'''SELECT shows.id, title, year, runtime, ROUND(rating, 2) AS rating, trailer, homepage
                        FROM shows
                        ORDER BY rating DESC
                        LIMIT 15 OFFSET {pagination}''')
    return cursor.fetchall()


@data_manager.connection_handler
def register(cursor, username, password):
    hashpsw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    good_hash = hashpsw.decode('utf-8')
    cursor.execute(f'''INSERT INTO registration(username, password)
                    VALUES (%(username)s, %(good_hash)s);''',
                   {'username': username, 'good_hash': good_hash})

@data_manager.connection_handler
def check_username_and_password(cursor, username, password):
    cursor.execute(""" SELECT password FROM registration
                        WHERE username= %(username)s""",
                   {'username': username})
    password_info = cursor.fetchone()
    if password_info is None:
        return False
    good_password = password_info['password']
    psw_match = bcrypt.checkpw(password.encode('utf-8'), good_password.encode('utf-8'))
    return psw_match


@data_manager.connection_handler
def get_user_id_for_comment(cursor, user_name):
    cursor.execute("""SELECT id from registration
                      WHERE username = %(user_name)s """,
                   {'user_name' : user_name})
    return cursor.fetchone()


@data_manager.connection_handler
def write_comment_info(cursor, user_id, show_id, comm):
    cursor.execute(f"""INSERT into comments (user_id, show_id, comment)
                     VALUES  ({user_id}, {show_id}, '{comm}')""")


@data_manager.connection_handler
def get_all_comment(cursor):
    cursor.execute(f"""SELECT comment, username FROM comments 
                        INNER JOIN registration ON registration.id = comments.user_id
    """)
    return cursor.fetchall()












