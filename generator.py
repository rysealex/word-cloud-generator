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
num_words = fc.get_validated_input("Enter number of words (1 < x <= 75): ", range(1, 76))
# subtract one from the related words to account for extra theme word
num_words -= 1

# check for related words
related_words = fc.get_related_words(theme_word, num_words)
if len(related_words) != num_words+1:
    print(f"Sorry, no related words found for {theme_word}.")
    print("Try a different word or a lower number of related words.")
    exit()

# get background color
#os.system('cls')
bkg_colors = ["white", "black", "gray"]
print("----------------------------------------------------------------------")
print("\tChoose a background color - [white=1, black=2, gray=3]")
print("----------------------------------------------------------------------")
bkg_color = fc.get_validated_input("Background color: ", range(1, 4))

# get colors
#os.system('cls')
colors = ["red", "blue", "green", "yellow", "purple", "orange"]
print("----------------------------------------------------------------------")
print("Choose colors - [red=1, blue=2, green=3, yellow=4, purple=5, orange=6]")
print("----------------------------------------------------------------------")
theme_color = fc.get_validated_input("Theme color: ", range(1, 7))
print("Choose three more colors - ")
color1 = fc.get_validated_input("Color one: ", range(1, 7))
color2 = fc.get_validated_input("Color two: ", range(1, 7))
color3 = fc.get_validated_input("Color three: ", range(1, 7))
other_colors = [colors[i-1] for i in [color1, color2, color3]]

# get font weight
#os.system('cls')
font_weights = ['light', 'normal', 'bold']
print("----------------------------------------------------------------------")
print("\tChoose a font weight - [light=1, normal=2, bold=3]")
print("----------------------------------------------------------------------")
font_weight = fc.get_validated_input("Font weight: ", range(1, 4))

# get font type
#os.system('cls')
font_types = ['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy']
print("-------------------------------------------------------------------------------")
print("Choose a font type - [serif=1, sans-serif=2, monospace=3, cursive=4, fantasy=5]")
print("-------------------------------------------------------------------------------")
font_type = fc.get_validated_input("Font type: ", range(1, 6))

# use spinner during generation
#os.system('cls')
spinner = Spinner("Generating word cloud...")
spinner.start()

try:
    # start timer
    start_time = time.time()

    # initiate the word cloud
    fc.basic_word_cloud(
        related_words, bkg_colors[bkg_color-1], colors[theme_color-1], other_colors, font_weights[font_weight-1], font_types[font_type-1]
    )

    # stop timer
    end_time = time.time()
finally:
    # always stop the spinner
    spinner.stop()

# display elapsed time
elapsed_time = end_time - start_time
print(f"\nElapsed time: {round(elapsed_time, 2)} seconds")