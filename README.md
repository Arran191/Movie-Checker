# Movie-Checker

Wanted to automate checking if a movie has been put on a streaming platform between the ones I am subscribed to. Initially wanted to check the Knowledge graph but couldn't do it, similarly couldn't find any reliable APIs that would do this for me.

Ended up taking a naive approach by web-scraping a Google Search for the movie. Checking the anchor HREF of the "Watch now" div which in turn would tell you which platform the movie is on. It isn't particularly robust but does the job for me.

## How to run

1. Create a python environment and install the requirements `pip install -r requirements.txt`
2. Run one of the below

### Run against CSV

To run against the CSV, simply run

`python Movie_Checker.py`

This will check what platforms the movies in the `WatchingList.csv` are on. If 'location' is filled in and there is a change this will be displayed.

### Run against Query

To run against a generic movie search, pass in `-q "move_name`

`python Movie_Checker -q "The 13th Warrior" -csv False`

### Check for changes

Pass in `-o True` to determine if the location of a movie has changed from what was previously recorded.

`python Movie_checker -o True`

#### To do

- Edit CSV to change the location of the movie.
- Add handle for if location is null
- Refactor messy code.
