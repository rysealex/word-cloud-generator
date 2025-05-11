import func as fc
import time
import sys
import threading
import os

'''
    -------------------------------------------------------------------------------------------------------
                                    Generator to start the word cloud process
    -------------------------------------------------------------------------------------------------------
'''

# Spinner class
class Spinner:
    def __init__(self, message="Generating..."):
        self.stop_running = False
        self.message = message
    
    def start(self):
        def spin():
            spinner_chars = ['|', '/', '-', '\\']
            idx = 0
            while not self.stop_running:
                sys.stdout.write(f'\r{self.message} {spinner_chars[idx % len(spinner_chars)]}')
                sys.stdout.flush()
                time.sleep(0.1)
                idx += 1
            os.system('cls')
            sys.stdout.write('\rFinished generating word cloud!')

        self.thread = threading.Thread(target=spin)
        self.thread.start()

    def stop(self):
        self.stop_running = True
        self.thread.join()

# start
print("----------------------------------------------------------------------")
print("\t\tWelcome to the word cloud generator!")
print("----------------------------------------------------------------------")
theme_word = input("Enter a theme word: ")

# check for valid word
if not fc.is_valid_word(theme_word):
    print("Please enter a real english word!")
    exit()

# get number of related words
try:
    num_words = int(input("Enter the number of related words (0 < # <= 100): "))
    if num_words < 1 or num_words > 100:
        print("Enter only numbers in range 1 to 100!")
        exit()
except ValueError:
    print("Enter only numbers in range 1 to 100!")
    exit()

# check for related words
related_words = fc.get_related_words(theme_word, num_words)
if len(related_words) != num_words+1:
    print(f"Sorry, no related words found for {theme_word}.")
    print("Try a different word or a lower number of related words.")
    exit()

# get background color
os.system('cls')
bkg_colors = ["white", "black", "gray"]
print("----------------------------------------------------------------------")
print("\tChoose a background color - [white=1, black=2, gray=3]")
print("----------------------------------------------------------------------")
try:
    bkg_color = int(input("Background color: "))
    if bkg_color < 1 or bkg_color > 3:
        print("Enter only numbers in range 1 to 3!")
        exit()
except ValueError:
    print("Enter only numbers in range 1 to 3!")
    exit()

# get colors
os.system('cls')
colors = ["red", "blue", "green", "yellow", "purple", "orange"]
print("----------------------------------------------------------------------")
print("Choose colors - [red=1, blue=2, green=3, yellow=4, purple=5, orange=6]")
print("----------------------------------------------------------------------")
try:
    theme_color = int(input("Theme color: "))
    if theme_color < 1 or theme_color > 6:
        print("Enter only numbers in range 1 to 6!")
        exit()
except ValueError:
    print("Enter only numbers in range 1 to 6!")
    exit()
print("Choose three more colors - ")
try:
    color1 = int(input("Color one: "))
    if color1 < 1 or color1 > 6:
        print("Enter only numbers in range 1 to 6!")
        exit()
    color2 = int(input("Color two: "))
    if color2 < 1 or color2 > 6:
        print("Enter only numbers in range 1 to 6!")
        exit()
    color3 = int(input("Color three: "))
    if color3 < 1 or color3 > 6:
        print("Enter only numbers in range 1 to 6!")
        exit()
except ValueError:
    print("Enter only numbers in range 1 to 6!")
    exit()

# get font weight
os.system('cls')
font_weights = ['light', 'normal', 'bold']
print("----------------------------------------------------------------------")
print("\tChoose a font weight - [light=1, normal=2, bold=3]")
print("----------------------------------------------------------------------")
try:
    font_weight = int(input("Font weight: "))
    if font_weight < 1 or font_weight > 3:
        print("Enter only numbers in range 1 to 3!")
        exit()
except ValueError:
    print("Enter only numbers in range 1 to 3!")
    exit()

# get font type
os.system('cls')
font_types = ['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy']
print("-------------------------------------------------------------------------------")
print("Choose a font type - [serif=1, sans-serif=2, monospace=3, cursive=4, fantasy=5]")
print("-------------------------------------------------------------------------------")
try:
    font_type = int(input("Font type: "))
    if font_type < 1 or font_type > 5:
        print("Enter only numbers in range 1 to 5!")
        exit()
except ValueError:
    print("Enter only numbers in range 1 to 5!")
    exit()

# use spinner during generation
os.system('cls')
spinner = Spinner("Generating word cloud...")
spinner.start()

try:
    # start timer
    start_time = time.time()

    # initiate the word cloud
    fc.basic_word_cloud(
        related_words, bkg_colors[bkg_color-1], colors[theme_color-1], colors[color1-1], 
        colors[color2-1], colors[color3-1], font_weights[font_weight-1], font_types[font_type-1]
    )

    # stop timer
    end_time = time.time()
finally:
    # always stop the spinner
    spinner.stop()

# display elapsed time
elapsed_time = end_time - start_time
print(f"\nElapsed time: {round(elapsed_time, 2)} seconds")