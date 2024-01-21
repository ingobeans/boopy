# Boopy

Boopy is a Pygame based game engine for Python. It's main focus is to be **intuitive** & to not need a lot of initializing.

## Installation

* Download boopy
* Run `pip install pygame-ce` (if you already have pygame installed, uninstall it. The pygame-ce version is a community made fork of pygame with improved performance and maintenance)
* In the boopy folder, run `pip install --upgrade .`

## Usage

Boopy folder includes an example project running boopy.

Otherwise, here is a general guide:
* Use `import boopy` to load boopy.
* Define your functions (including one update function which will be called every frame), classes and everything which needs defining.
* Here you should probably also define your sprites, spritesheets and tilemaps.
* In your functions you can use `boopy.btn()` to check for keys being pressed. Pass a key, ex. `boopy.K_RIGHT` or `boopy.K_d`, or a list of keys to check.
* You can also use `boopy.btnp()` to only check for buttons just pressed.
* Finally, use boopy.run() to run the game. The run function requires a reference to your games update function. If you're encountering stuttering I recommend turning off the FPS cap and enabling VSync.