import cv2
from PIL import ImageGrab, Image
import pyautogui
from time import sleep
import pytesseract
import appscript
import numpy as np
import anagram
from pynput import mouse


terminate = False


def get_window():
    app = appscript.app('System Events').application_processes['iPhone Mirroring']
    position = app.windows[0].position()
    size = app.windows[0].size()
    return position, size



def grab_bottom(position, size):
    ImageGrab.grab(bbox=(position[0], position[1]+(int(2 * (size[1] / 3))), position[0]+size[0], position[1]+size[1])).save('bottom.png')

def img_process():
    img = cv2.imread('bottom.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = np.array(gray)
    #set all colors to white but the text to black
    converted = np.where(data > 10, 255, 0)
    converted = np.array(converted)
    img = Image.fromarray(converted.astype('uint8'))
    img.save('bottom.png')

def create_coords(position, size):
    coords = []
    y = .82*size[1]
    for i in range(12):
        if i % 2 == 1:
            coords.append((position[0] + ((i/12) * size[0]), position[1] + y))
    return coords

def get_letters():
    text = pytesseract.image_to_string('bottom.png')
    text.replace(" ", "")
    if len(text) != 6:
        print("OCR no work")
        text = input("type letters for anagrams: ")
    text = text.upper()
    return text

def get_combos(text):
    combos1 = anagram.find_anagrams(text)
    combos = []
    #remove duplciate letters
    [combos.append(x) for x in combos1 if x not in combos]
    return combos

def map_letters_to_coords(text, coords):
    map = {}
    for letter in text:
        if letter in map:
            map[letter + letter] = coords.pop(0)
        else:
            map[letter] = coords.pop(0)
    return map

#check if mouse is clicked
def on_click(x, y, button, pressed):
    if not pressed:
        # Stop listener
        return False


def move_mouse(map, combo, position, size):
    letters_entered = []
    for letter in combo:
        if letter not in letters_entered:
            letters_entered.append(letter)
            pyautogui.moveTo(map[letter])
        else:
            letters_entered.append(letter + letter)
            pyautogui.moveTo(map[letter + letter])
        #wait until mouse is clicked
        with mouse.Listener(
            on_click=on_click) as listener:
            listener.join()
    pyautogui.moveTo(position[0] + int(size[0]/2), position[1] + int(size[1]*.6))
    with mouse.Listener(
            on_click=on_click) as listener:
        listener.join()

def main():
    for i in range (3):
        print(3-i)
        sleep(1)
    position, size = get_window()
    grab_bottom(position, size)
    img_process()
    text = get_letters()
    combos = get_combos(text)
    print(combos)
    coords = create_coords(position, size)
    map = map_letters_to_coords(text, coords)
    for combo in combos:
        if terminate:
            break
        print(str(combo))
        move_mouse(map, combo, position, size)
    print("done")

if __name__ == "__main__":
    main()    