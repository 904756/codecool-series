from flask import Flask, render_template, url_for
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool-series-v2')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/most-rated')
def most_rated_shows():
    most_rated = queries.get_most_rated_shows()
    no_link = 'No URL'
    return render_template('most-rated-shows.html', most_rated_shows=most_rated, no_link=no_link)


@app.route('/show/<int:show_id>')
def show_page(show_id):
    show_details = queries.get_show_details_by_id(show_id)
    return render_template('show-page.html', show_id=show_id, show_details=show_details)


def main():
    # app.run(debug=False)
    app.run(
        host="0.0.0.0",
        debug=True)


if __name__ == '__main__':
    main()
