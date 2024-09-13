# maple-bindings
An input display setup for Maplestory

Original program from https://www.reddit.com/r/Maplestory/comments/q50xdr/streamers_i_made_a_keyboard_overlay_for_skills/ , though link seems to have been deleted
I (Serp/Mach) have made a few of my own modifications:

- Keys light up when held instead of getting spammed
- The arrows.png file has been modified to have the color indicators on the left, so it's easier to read when they overlap

- The bindings folder holds alternate keybinds for your mules or training/farming; feel free to empty it and replace it with your own
- - When running the program (step 8 below), you can do "python3 moverly.py [filename]" to load the corresponding overlay in the bindings directory (don't need to include .png)
- - When the program is already running, you can use Ctrl+Shift+F1 to select a new overlay to use
- - I added a way to load and switch between multiple bindings at once to support Beast Tamer, but they're ded so probably not relevant
- You can press Ctrl+Shift+F3 to "freeze" or "unfreeze" the reading, so you don't accidentally leak stuff typing while recording

--------------------------
*(Instructions from original author)*

This code is provided as is. Use at your own risk.

## How to use with OBS Studio
0. As with all keyboard overlays, BE CAREFUL not to type any sensitive information while MOverlay is running. *(MODIFICATION NOTE: Remember to use the "freeze" command if you need to)*
### Set Up
1. Download this file and save it as moverlay.py. Make sure you have "file name extensions" turned on in Windows.
2. Take a screenshot of your key bindings in game and save it AS A PNG FILE. Rename it to bindings.png and save it to the same folder as moverlay.py.
3. Download the image called magic.png at https://postimg.cc/V018VWLz and save it to the same folder as moverlay.py.
4. Install the latest Python 3.9.
5. Open Command Prompt. Run the command "pip3 install numpy opencv-python pillow pynput" (without quotes) and answer Y to the prompts. This will install dependencies.
### Running MOverlay
6. Run a new Command Prompt AS ADMINISTRATOR*. Step by step: press the Windows key, search for Command Prompt, right click it, click Run as administrator.
7. In the admin Command Prompt, change directory (cd) to the folder that contains moverlay.py. For example, if I saved the files to Downloads, I would run the command "cd C:\Users\%USERNAME%\Downloads" (without quotes).
8. In the admin Command Prompt, run the command "python3 moverlay.py" (without quotes).
9. Add the MOverlay window as a new source in OBS. Use the chroma key filter to remove the green. Resize it to your liking.

*Command prompt must be run as administrator to read your key input while you're in the game.
