import glob
import os
from urllib.parse import urlparse

from flask import Flask, abort, request, redirect

from decorators import ip_filtered
from misc import *


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
            <h3><a style="color: gray;" href="/shows/{show}">{show.capitalize()}</a></h3>
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
            <h3><a style="color: gray;" href="/shows/{show}/s{number}">Season {number}</a></h3>
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
            <h3><a style="color: gray;" href="/play/{show}/{season}/e{number}">Episode {number}</a></h3>
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
                                                    video_path=video_path,
                                                    show=show
                                                    )
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)


@server.route("/playnext")
@server.route("/playnext/")
def play_next_episode():
    referrer = request.referrer
    if referrer is None:
        return "You did not go to this page from a previous episode so we cannot find the next episode."
    else:
        path = [item for item in urlparse(referrer).path.split("/") if item != ""]
        if len(path) == 4:
            show = path[1]
            season = path[2]
            episode = path[3]
            season_episodes = get_folder_files(f"static/shows/{show}/{season}")
            next_episode_num = int(episode[1]) + 1
            next_episode = f"e{next_episode_num}"
            if next_episode + ".mp4" in season_episodes:
                return redirect(f"/../play/{show}/{season}/{next_episode}")
            else:
                seasons = get_sub_folders(f"static/shows/{show}")
                next_season_num = int(season[1]) + 1
                next_season = f"s{next_season_num}"
                if next_season in seasons:
                    next_season_episodes = get_folder_files(f"static/shows/{show}/{next_season}")
                    next_episode = os.path.splitext(next_season_episodes[0])[0]
                    return redirect(f"/../play/{show}/{next_season}/{next_episode}")
                else:
                    return f"<h1 style=\"font-family: arial;\">You have finished watching all episodes for {show}. Sorry!</h1>"


if __name__ == "__main__":
    server.run(port="80", host="0.0.0.0")
