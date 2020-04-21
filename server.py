import glob
import os

from flask import Flask, abort, request, Response

from decorators import ip_filtered


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_sub_folders(folder):
    return [f for f in sorted(os.listdir(folder)) if os.path.isdir(os.path.join(folder, f))]


def get_folder_files(folder):
    return [f for f in sorted(os.listdir(folder)) if os.path.isfile(os.path.join(folder, f)) and f.endswith(".mp4")]


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


server = Flask(__name__)


@server.route("/")
@server.route("/home")
@server.route("/home/")
@ip_filtered
def home():
    return get_file("views/home.html")


@server.route("/shows/")
@server.route("/shows")
@ip_filtered
def list_shows():
    shows = get_sub_folders("static/shows")
    formatted_shows = []
    for show in shows:
        f = f'''
            <a style="color: gray;" href="/shows/{show}">{show.capitalize()}</a>
            <br />
            '''
        formatted_shows.append(f)
    formatted_shows = " ".join(formatted_shows)
    html = get_file("views/shows.html").format(shows=formatted_shows)
    return html


@server.route("/shows/<string:show>")
@server.route("/shows/<string:show>/")
@ip_filtered
def list_seasons(show):
    season_numbers = [season[1] for season in get_sub_folders(f"static/shows/{show}")]
    formatted_seasons = []
    for number in season_numbers:
        f = f'''
            <a style="color: gray;" href="/shows/{show}/s{number}">Season {number}</a>
            <br />
            '''
        formatted_seasons.append(f)
    formatted_seasons = " ".join(formatted_seasons)
    html = get_file("views/seasons.html").format(show_capital=show.capitalize(), seasons=formatted_seasons)
    return html


@server.route("/shows/<string:show>/<string:season>")
@server.route("/shows/<string:show>/<string:season>/")
@ip_filtered
def list_episodes(show, season):
    episode_numbers = [episode[1] for episode in get_folder_files(f"static/shows/{show}/{season}")]
    formatted_episodes = []
    for number in episode_numbers:
        f = f'''
            <a style="color: gray;" href="/play/{show}/{season}/e{number}">Episode {number}</a>
            <br />
            '''
        formatted_episodes.append(f)
    formatted_episodes = " ".join(formatted_episodes)
    html = get_file("views/episodes.html").format(
                                            show_capital=show.capitalize(), 
                                            season=season, 
                                            season_num=season[1],
                                            episodes=formatted_episodes,
                                            show=show
                                            )
    return html
    

@server.route("/play/<string:show>/<string:season>/<string:episode>")
@server.route("/play/<string:show>/<string:season>/<string:episode>/")
@ip_filtered
def play_show_episode(show, season, episode):
    valid_shows = get_sub_folders("static/shows")
    show_capital = show.capitalize()
    season_num = season[1]
    episode_num = episode[1]
    if show in valid_shows:
        valid_seasons = get_sub_folders(f"static/shows/{show}")
        if season in valid_seasons:
            valid_episodes = get_folder_files(f"static/shows/{show}/{season}")
            if episode + ".mp4" in valid_episodes:
                video_path = f"{show}/{season}/{episode}"
                season_path = f"{show}/{season}"
                return get_file("views/video.html").format(   
                                                    show_capital=show_capital,
                                                    season_num=season_num,
                                                    episode_num=episode_num,
                                                    season_path=season_path,
                                                    video_path=video_path
                                                    )
            else:
                return f"<h2>{show_capital} does not have Season {season[1]} Episode {episode[1]} on the server.</h2>"
        else:
            return f"<h2>{show_capital} does not have Season {season[1]} on the server.</h2>"
    else:
        return f"<h2>The show \"{show}\" was not found on the server. Did you type it correctly?</h2>"


if __name__ == "__main__":
    server.run(port="80", host="0.0.0.0")
