from flask import Flask, render_template, url_for, jsonify
from data import queries
import math
from dotenv import load_dotenv


load_dotenv()
app = Flask('codecool-series-v2')
SHOWS_PER_PAGE = 15
SHOWN_PAGE_NUMBERS = 5


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/')
@app.route('/shows/<int:page_number>')
@app.route('/shows/most-rated/')
@app.route('/shows/most-rated/<int:page_number>')
@app.route('/shows/order-by-<order_by>/')
@app.route('/shows/order-by-<order_by>-<order>/')
@app.route('/shows/order-by-<order_by>/<int:page_number>')
@app.route('/shows/order-by-<order_by>-<order>/<int:page_number>')
def most_rated_shows(page_number=1, order_by="rating", order="DESC"):
    count = queries.get_show_count()
    pages_count = math.ceil(count[0]['count'] / SHOWS_PER_PAGE)
    shows = queries.get_shows_limited(order_by, order, SHOWS_PER_PAGE, (page_number - 1) * SHOWS_PER_PAGE)
    print(shows)
    shown_pages_start = int(page_number - ((SHOWN_PAGE_NUMBERS - 1) / 2))
    shown_pages_end = int(page_number + ((SHOWN_PAGE_NUMBERS - 1) / 2))
    if shown_pages_start < 1:
        shown_pages_start = 1
        shown_pages_end = SHOWN_PAGE_NUMBERS
    elif shown_pages_end > pages_count:
        shown_pages_start = pages_count - SHOWN_PAGE_NUMBERS + 1
        shown_pages_end = pages_count
    return render_template(
        'most-rated-shows.html',
        shows=shows,
        pages_count=pages_count,
        page_number=page_number,
        shown_pages_start=shown_pages_start,
        shown_pages_end=shown_pages_end,
        order_by=order_by,
        order=order
    )


@app.route('/show/<show_id>')
def show_page(show_id):
    show_details = queries.get_show_details_by_id(show_id)
    seasons = queries.get_list_seasons(show_id)
    no_overview = 'No description available'
    top_3_actors = queries.get_top_3_actors(show_id)
    for detail in show_details:
        if detail['trailer'] is None:
            video_id = ''
        else:
            video_id = show_details[0]["trailer"][27:]
    return render_template('show-page.html',
                           show_id=show_id,
                           show_details=show_details,
                           seasons=seasons,
                           video_id=video_id,
                           no_overview=no_overview,
                           top_3_actors=top_3_actors)


@app.route('/get-actors-less-than-10-shows')
def display_actors_less_than_10_shows():
    actors = queries.get_actors()
    return render_template('actors.html', actors=actors)


# @app.route('/api/get-actor-year/<year>')
# def display_actor_year(year):
#     years = queries.get_years()
#     return jsonify(years)


@app.route('/seasons')
def display_season():
    seasons = queries.get_seasons()
    return render_template('seasons.html', seasons=seasons)


@app.route('/api/get-episodes/<title>')
def get_episodes(title):
    episodes = queries.get_episodes(title)
    return jsonify(episodes)


@app.route('/display-actors')
def get_actors():
    actors = queries.get_show_actors()
    return render_template('actors-shows.html', actors=actors)


def main():
    app.run(
        host="0.0.0.0",
        port=5000)


if __name__ == '__main__':
    main()
