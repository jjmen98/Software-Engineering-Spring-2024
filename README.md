# Team 16 Photon README

## About

This project is a modern replica of the software for Photon, a laser tag game created in March 1984, made in Python.
This is being developed for Ubuntu 22.04 systems, though will work on any system with a Python interpreter.

## Team 16 Members

| GitHub        | Real Name       |
| ------------- | --------------- |
| @sanpdy       | Sankalp Pandey  |
| @jjmen98      | Jonathan Mendez |
| @amwells-git  | Alexander Wells |
| @bmwodka      | Benjamin Wodka  |
| @recolaa      | Haden Fowler    |
| @GabeKincade  | Gabriel Kincade |
| @TheGreatestt | Brad Daugherty  |


## Required Python Packages

This Python project uses Supabase open-source python integration, PyQt6, Pygame, and the python-dotenv packages.
All of these packages can be found & installed by pip

*Supabase*

>pip install supabase

*PyQt6*

>pip install PyQt6

*Pygame*

>pip install pygame

*python-dotenv*

>pip install python-dotenv

## Running the Program

To run this project, download & extract the main branch to a directory on your system

Then, run your Python3 compiler from the extracted folder containing main.py using

>python3 main.py

### Player Entry:
- To add a player, input their unique player ID, a codename, and their associated equipment ID.
- Click the Save button corresponding to the player's team.
- If the player ID is recognized, their codename will be updated from the database; otherwise, a new entry will be created.
- To clear player entries, either click "Delete Game" or press F12.

### Starting the Game:
- Once all players and their details are entered, click "Start Game" or press F5.
- This will initiate a 30-second countdown before transitioning to the Game Action screen.

### Game Action:
- This screen displays player codenames and their scores for the ongoing game.

## Known Issues

There is a PyQt6 implementation of the splash screen in the source code, however, there is an issue displaying it on Ubuntu 22.04.

This is currently attributed to a failed communication between Ubuntu and the PyQt6 package.

Currently, the splash screen is handled by Pygame, though we are working diligently to get the PyQt6 implementation working to lessen the required packages.

## Future Changes

1. Allow Player ID lookup without Codename & Equipment ID fields filled
2. Handle Duplicate Player Input
3. Add Play & Countdown Screens
4. Update Backend to handle Score & Hit tracking
