from flask import Flask, render_template, url_for, request, redirect, session
from data import queries
import data_manager

app = Flask('codecool_series')
app.config["SECRET_KEY"] = 'PQHL-_RyvW8-rlGvakZUBQ'


@app.route('/')
def index():
    page_id = 1
    shows = queries.get_shows_direction()
    genres = queries.get_genre()
    print(shows)
    return render_template('index.html', shows=shows, page_id=page_id, genres=genres, i=0)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        queries.register(username,password)
    return redirect('/')


@app.route('/sign-in', methods=['GET', 'POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    match = queries.check_username_and_password(user, password)
    if match:
        session['USERNAME'] = user
        return redirect('/')
    else:
        return redirect('/')


@app.route('/show/<int:show_id>')
def get_show(show_id):
    show_info = queries.get_show(show_id)
    video_id = None
    if show_info:
        if show_info['trailer'] is None:
            video_id = None
        else:
            video_id = show_info['trailer'].split('v=')[1]
    actors = queries.get_actors(show_id)
    seasons = queries.get_seasons(show_id)
    all_comments = queries.get_all_comment()
    return render_template('design.html', show_info=show_info, video_id=video_id, actors=actors, seasons=seasons, show_id=show_id, all_comments=all_comments)


@app.route('/page/<int:page_id>')
def pagination(page_id):
    pagination = (page_id -1) * 16
    shows = queries.get_page(pagination)
    genres = queries.get_genre()
    return render_template('index.html', page_id=page_id, shows=shows, genres=genres, i=0)


@app.route('/<int:page_id>/sort-by/<order>/<direction>')
def resorting(page_id, order, direction):
    pagination = (page_id -1) * 16
    if order == "genre":
        genres = queries.genre_sort(direction)
        shows = queries.get_page(pagination)
    else:
        shows = queries.resorting(pagination, order, direction)
        genres = queries.get_genre()
    return render_template('index.html', page_id=page_id, shows=shows, genres=genres, i=0)


@app.route('/log-out')
def log_out():
    session.pop('USERNAME')
    return redirect('/')

@app.route('/add-comment/<int:show_id>', methods=['POST'])
def comment(show_id):
    comment = request.form['my_comment']
    user_id = queries.get_user_id_for_comment(session['USERNAME'])['id']
    queries.write_comment_info(user_id, show_id, comment)
    return redirect('/show/' + str(show_id))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
