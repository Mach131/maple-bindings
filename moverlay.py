# This code is provided as is. Use at your own risk.
#
# How to use with OBS Studio
# --------------------------
# 0. As with all keyboard overlays, BE CAREFUL not to type any sensitive information while MOverlay is running.
# Set Up
# 1. Download this file and save it as moverlay.py. Make sure you have "file name extensions" turned on in Windows.
# 2. Take a screenshot of your key bindings in game and save it AS A PNG FILE. Rename it to bindings.png and save it to the same folder as moverlay.py.
# 3. Download the image called magic.png at https://postimg.cc/V018VWLz and save it to the same folder as moverlay.py.
# 4. Install the latest Python 3.9.
# 5. Open Command Prompt. Run the command "pip3 install numpy opencv-python pillow pynput" (without quotes) and answer Y to the prompts. This will install dependencies.
# Running MOverlay
# 6. Run a new Command Prompt AS ADMINISTRATOR*. Step by step: press the Windows key, search for Command Prompt, right click it, click Run as administrator.
# 7. In the admin Command Prompt, change directory (cd) to the folder that contains moverlay.py. For example, if I saved the files to Downloads, I would run the command "cd C:\Users\%USERNAME%\Downloads" (without quotes).
# 8. In the admin Command Prompt, run the command "python3 moverlay.py" (without quotes).
# 9. Add the MOverlay window as a new source in OBS. Use the chroma key filter to remove the green. Resize it to your liking.
#
# *Command prompt must be run as administrator to read your key input while you're in the game.


# Original program from https://www.reddit.com/r/Maplestory/comments/q50xdr/streamers_i_made_a_keyboard_overlay_for_skills/ , though link seems to have been deleted
# I (Serp/Mach) have made a few of my own modifications:
#
# - Keys light up when held instead of getting spammed
# - The arrows.png file has been modified to have the color indicators on the left, so it's easier to read when they overlap
#
# - The bindings folder holds alternate keybinds for your mules or training/farming; feel free to empty it and replace it with your own
# --- When running the program (step 8), you can do "python3 moverly.py [filename]" to load the corresponding overlay in the bindings directory (don't need to include .png)
# --- When the program is already running, you can use Ctrl+Shift+F1 to select a new overlay to use
# --- I added a way to load and switch between multiple bindings at once to support Beast Tamer, but they're ded so probably not relevant
# - You can press Ctrl+Shift+F3 to "freeze" or "unfreeze" the reading, so you don't accidentally leak stuff typing while recording

import tkinter as tk
from tkinter.filedialog import askopenfilenames
from datetime import datetime, timedelta
from PIL import Image, ImageTk, ImageDraw
from pynput import keyboard
import cv2
import numpy as np
import sys

## SETTINGS
CLEAR_ROW_MILLIS = 3000
NEW_ROW_MILLIS = 420
ROW_HEIGHT_PX = 40
ROW_WIDTH_PX = 400
MAGIC_FILE = 'magic.png'
BINDINGS_FILE = 'bindings.png'
ARROWS_FILE = 'arrows.png'
MAX_WRAP_ROWS = 3
##

class LabelRow:
    def __init__(self, now):
        self.labels = []
        self.start_time = now
        self.last_active = now
        self.num_rows = 0
    def add_label(self, label, now):
        self.labels.append((label, now))
        self.last_active = now
        
        total_width = (now - self.start_time).total_seconds() * 300
        self.num_rows = (total_width // (ROW_WIDTH_PX - ICON_SIZE)) + 1
        if self.num_rows > MAX_WRAP_ROWS:
            self.prune_row()
    def prune_row(self):
        cutoff_time = self.start_time + timedelta(seconds=(ROW_WIDTH_PX - ICON_SIZE)/300)
        removed = 0
        for label, timestamp in self.labels:
            if timestamp > cutoff_time:
                break
            label.destroy()
            removed += 1
        self.labels = self.labels[removed:]
        self.start_time = cutoff_time
    def destroy(self):
        for label, _ in self.labels:
            label.destroy()
    def reposition(self, y, wraparound):
        xoffset = 0
        for label, timestamp in self.labels:
            xpos = (timestamp - self.start_time).total_seconds() * 300
            if xpos - xoffset > wraparound:
                y += ROW_HEIGHT_PX
                xoffset += wraparound
            label.place(x = xpos - xoffset, y = y)
        return y + ROW_HEIGHT_PX

class LabelGrid:
    def __init__(self):
        self.last_active = 0
        self.rows = []
    def add_label(self, label, now):
        if len(self.rows) == 0 or \
           now - self.last_active > timedelta(milliseconds = NEW_ROW_MILLIS):
            self.rows.append(LabelRow(now))
        self.rows[-1].add_label(label, now)
        self.last_active = now
        return self.rows[-1]
    def reposition(self, now, wraparound):
        kept_rows = []
        for row in self.rows:
            if now - row.last_active > timedelta(milliseconds = CLEAR_ROW_MILLIS):
                row.destroy()
            else:
                kept_rows.append(row)
        self.rows = kept_rows
        y = 0
        for row in self.rows:
            y = row.reposition(y = y, wraparound = wraparound)
    def clear(self):
        for row in self.rows:
            row.destroy()
        self.rows = []

def find_origin():
    magic = cv2.imread(MAGIC_FILE)
    bindings = cv2.imread(BINDINGS_FILE)
    res = cv2.matchTemplate(bindings, magic, cv2.TM_SQDIFF)
    return np.unravel_index(res.argmin(), res.shape)

keys = {}
arrow_keys = {}

keys['Key.esc'] = (0, 0)
keys['Key.f1'] = (0, 2)
keys['Key.f2'] = (0, 3)
keys['Key.f3'] = (0, 4)
keys['Key.f4'] = (0, 5)
keys['Key.f5'] = (0, 6.5)
keys['Key.f6'] = (0, 7.5)
keys['Key.f7'] = (0, 8.5)
keys['Key.f8'] = (0, 9.5)
keys['Key.f9'] = (0, 11)
keys['Key.f10'] = (0, 12)
keys['Key.f11'] = (0, 13)
keys['Key.f12'] = (0, 14)

keys[192] = (1, 0) # `
keys[49] = (1, 1) # 1
keys[50] = (1, 2) # 2
keys[51] = (1, 3) # 3
keys[52] = (1, 4) # 4
keys[53] = (1, 5) # 5
keys[54] = (1, 6) # 6
keys[55] = (1, 7) # 7
keys[56] = (1, 8) # 8
keys[57] = (1, 9) # 9
keys[48] = (1, 10) # 0
keys[189] = (1, 11) # -
keys[187] = (1, 12) # =

keys[81] = (2, 1.5) # q
keys[87] = (2, 2.5) # w
keys[69] = (2, 3.5) # e
keys[82] = (2, 4.5) # r
keys[84] = (2, 5.5) # t
keys[89] = (2, 6.5) # y
keys[85] = (2, 7.5) # u
keys[73] = (2, 8.5) # i
keys[79] = (2, 9.5) # o
keys[80] = (2, 10.5) # p
keys[219] = (2, 11.5) # [
keys[221] = (2, 12.5) # ]
keys[220] = (2, 13.75) # \

keys[65] = (3, 2) # a
keys[83] = (3, 3) # s
keys[68] = (3, 4) # d
keys[70] = (3, 5) # f
keys[71] = (3, 6) # g
keys[72] = (3, 7) # h
keys[74] = (3, 8) # j
keys[75] = (3, 9) # k
keys[76] = (3, 10) # l
keys[186] = (3, 11) # ;
keys[222] = (3, 12) # '

keys['Key.shift'] = (4, 0.75)
keys['Key.shift_l'] = (4, 0.75)
keys['Key.shift_r'] = (4, 0.75)
keys[90] = (4, 2.5) # z
keys[88] = (4, 3.5) # x
keys[67] = (4, 4.5) # c
keys[86] = (4, 5.5) # v
keys[66] = (4, 6.5) # b
keys[78] = (4, 7.5) # n
keys[77] = (4, 8.5) # m
keys[188] = (4, 9.5) # ,
keys[190] = (4, 10.5) # .

keys['Key.ctrl'] = (5, 0.25)
keys['Key.ctrl_l'] = (5, 0.25)
keys['Key.ctrl_r'] = (5, 0.25)
keys['Key.alt'] = (5, 3.25)
keys['Key.alt_l'] = (5, 3.25)
keys['Key.alt_r'] = (5, 3.25)
keys['Key.alt_gr'] = (5, 3.25)
keys['Key.space'] = (5, 7)

keys['Key.scroll_lock'] = (0, 16.25)
keys['Key.insert'] = (1, 15.25)
keys['Key.home'] = (1, 16.25)
keys['Key.page_up'] = (1, 17.25)
keys['Key.delete'] = (2, 15.25)
keys['Key.end'] = (2, 16.25)
keys['Key.page_down'] = (2, 17.25)

arrow_keys['Key.up'] = (0, 1)
arrow_keys['Key.left'] = (1, 0)
arrow_keys['Key.down'] = (1, 1)
arrow_keys['Key.right'] = (1, 2)

origin = find_origin()

ICON_SIZE = 32
ICON_MARGIN = 1
OFFSET_X = -1
OFFSET_Y = -104

FADE_MASK = Image.new("RGB", (ICON_SIZE, ICON_SIZE), (0, 0, 0))

def keyid(key):
    if hasattr(key, 'vk'):
        return key.vk
    else:
        return str(key)
    return None

def crop_key(kid, key_array=keys):
    oy, ox = origin
    r, c = key_array[kid]
    x = int(ox + c * (ICON_SIZE + ICON_MARGIN) + OFFSET_X + 1e-3)
    y = int(oy + r * (ICON_SIZE + ICON_MARGIN) + OFFSET_Y + 1e-3)
    if r == 0:
        y -= 5
    if r == 0 and c > 6 and c < 10:
        x += 1
    if c > 14:
        x += 1
    if r == 2 and c == 13.75:
        x += 1
    if r == 3 or r == 4 or (r == 5 and c != 0.25):
        x -= 1
    return (x, y, x + ICON_SIZE, y + ICON_SIZE)

def key_tkimage(bindings, kid, key_array=keys):
    img = bindings.crop(crop_key(kid, key_array))
    green = (0, 255, 0)
    ImageDraw.floodfill(img, (0            , 0), green)
    ImageDraw.floodfill(img, (ICON_SIZE - 1, 0), green)
    ImageDraw.floodfill(img, (0            , ICON_SIZE - 1), green)
    ImageDraw.floodfill(img, (ICON_SIZE - 1, ICON_SIZE - 1), green)

    img_f = Image.blend(img, FADE_MASK, 0.3)

    return (ImageTk.PhotoImage(img), ImageTk.PhotoImage(img_f))

BT_TESTING = False
CAT_BINDINGS_FILE = ''
BEAR_BINDINGS_FILE = ''

if __name__ == "__main__":
    if len(sys.argv) > 1:
        BINDINGS_FILE = 'bindings/' + sys.argv[1] + '.png'
        if len(sys.argv) > 2:
            CAT_BINDINGS_FILE = 'bindings/' + sys.argv[2] + '.png'
            if len(sys.argv) > 3:
                BEAR_BINDINGS_FILE = 'bindings/' + sys.argv[3] + '.png'
            BT_TESTING = True

    root = tk.Tk()
    root.title('MOverlay')
    root.geometry(str(ROW_WIDTH_PX) + "x500")
    root.configure(background='#00ff00')

    all_keys = list(keys.keys()) + list(arrow_keys.keys())

    arrows = Image.open(ARROWS_FILE)
    tk_arrow_keys = {kid: key_tkimage(arrows, kid, arrow_keys) for kid in arrow_keys}

    grid = LabelGrid()

    (bindings, tk_keys, pressed_keys, shift_check) = (None,) * 4
    (cat_bindings, bear_bindings, tk_hawk_keys, tk_cat_keys, tk_bear_keys) = (None,) * 5

    def init_bindings():
        global grid, bindings, tk_keys, pressed_keys, shift_check, cat_bindings, \
            bear_bindings, tk_hawk_keys, tk_cat_keys, tk_bear_keys

        grid.clear()
        bindings = Image.open(BINDINGS_FILE).resize((622, 232))
        tk_keys = {kid: key_tkimage(bindings, kid) for kid in keys}

        pressed_keys = {}

        if BT_TESTING:
            cat_bindings = Image.open(CAT_BINDINGS_FILE)
            bear_bindings = Image.open(BEAR_BINDINGS_FILE)
            tk_hawk_keys = tk_keys
            tk_cat_keys = {kid: key_tkimage(cat_bindings, kid) for kid in keys}
            tk_bear_keys = {kid: key_tkimage(bear_bindings, kid) for kid in keys}
            shift_check = False

    init_bindings()
    muted = False

    def on_press(key):
        global grid, bindings, tk_keys, pressed_keys, shift_check, cat_bindings, \
            bear_bindings, tk_hawk_keys, tk_cat_keys, tk_bear_keys, muted, \
            BT_TESTING, BINDINGS_FILE, CAT_BINDINGS_FILE, BEAR_BINDINGS_FILE
        
        kid = keyid(key)
        if kid is None or kid not in all_keys or kid in pressed_keys:
            return

        if 'Key.shift' in pressed_keys and 'Key.ctrl_l' in pressed_keys:
            if kid == 'Key.f1':
                binding_files = askopenfilenames()
                pressed_keys = {}

                if len(binding_files) == 0:
                    return

                bindings.close()
                if (BT_TESTING):
                    cat_bindings.close()
                    bear_bindings.close()

                BINDINGS_FILE = binding_files[-1]
                if len(binding_files) > 1:
                    CAT_BINDINGS_FILE = binding_files[-2]
                    if len(binding_files) > 2:
                        BEAR_BINDINGS_FILE = binding_files[-3]
                    BT_TESTING = True
                else:
                    BT_TESTING = False

                init_bindings()
                return

            if kid == "Key.f3":
                muted = not muted

        
        if BT_TESTING:
            if kid == 'Key.shift':
                shift_check = True
            elif shift_check and kid in tk_arrow_keys:
                if kid == 'Key.up':
                    tk_keys = tk_hawk_keys
                if kid == 'Key.down':
                    tk_keys = tk_cat_keys
                if kid == 'Key.left' and BEAR_BINDINGS_FILE != '':
                    tk_keys = tk_bear_keys
                shift_check = False

        if muted:
            pressed_keys[kid] = None
            return
        img = tk_keys[kid] if kid in tk_keys else tk_arrow_keys[kid]
        label = tk.Label(root, image = img[0], borderwidth=0)
        now = datetime.now()
        row = grid.add_label(label = label, now = now)
        grid.reposition(now = now, wraparound = ROW_WIDTH_PX - ICON_SIZE)
        pressed_keys[kid] = (label, row, img[1])

    def on_release(key):
        kid = keyid(key)
        if kid is None or kid not in all_keys:
            return
        if kid in pressed_keys:
            key_data = pressed_keys.pop(kid)
            if key_data is not None:
                label, row, img_f = key_data
                if label.winfo_exists():
                    label.configure(image = img_f)
                else:
                    new_label = tk.Label(root, image = img_f, borderwidth=0)
                    now = datetime.now()
                    grid.add_label(label = new_label, now = now)
                    grid.reposition(now = now, wraparound = ROW_WIDTH_PX - ICON_SIZE)


    listener = keyboard.Listener(on_press = on_press, on_release = on_release)
    listener.start()
    root.mainloop()
