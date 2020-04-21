# Python-Video-Server
A flask server to server mp4 to a whitelisted set of users based on IP address.

## Setup
Add your public IPV4 in a file called `ips.txt` in the root of the server directory. Inside, place IPs like this:

	ip.1.goes.here,
	ip.2.goes.here

**Each new ip requires a comma after the last ip, a new line and no comma at the end of the last IP (similar to JSON)**

Then you need to do the following:

1. `pip install virtualenv`
2. `virtualenv python_video_server`
3. Activate the virtualenv (google it)
4. `pip install flask`
5. `python server.py`

## Adding content

### Adding a show
1. Make a folder called `shows` inside the `static` folder
2. Make a folder inside `shows` named whatever the show is named. Example: `letterkenny`
3. Make a folder for each season that follows the pattern `sn` for each season of the show where `n` = season number.
4. Upload the `.mp4` files into the season folder and name them `en.mp4` where `n` = episode number
5. Go to `/shows` and verify the new show is there and all its content. If not, double check you did exactly what was required.

### Adding a movie
1. Make a folder called `movies` inside the `static` folder
2. Make a folder inside `movies` and call it something recognizable. Example: `nacholibre`
3. Make a file called `title.txt` inside the recognizable folder. On the first line of it, write the title of the movie. Example: `Nacho Libre`
4. Upload the `.mp4` file in the same folder and call it `movie.mp4`
5. Go to `/movies` and verify the new movie is listed there. If not, double check you did exactly what was required.

Example directory tree:

	.
	+--static
		|
		+--shows
		|   |
		|   +--letterkenny
		|       | 
		|       +--s1
		|           |
		|           +--e1.mp4
		|           |
		|           +--e2.mp4
		+--movies
		|	|
		|	+--nacholibre
		|		|
		|		+--title.txt
		|		|
		|		+--movie.mp4
