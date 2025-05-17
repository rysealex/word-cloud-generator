from rtree import index
import numpy as np
import matplotlib.pyplot as plt
import random
import requests
import os
from io import BytesIO

'''
    -------------------------------------------------------------------------------------------------------
                                            Basic word cloud generator
    -------------------------------------------------------------------------------------------------------
'''

DEBUG_MODE = False
STATISTICS_MODE = False

'''
    Checks for valid user inputs, displays error message and exits if invalid
    Returns the user input if valid
'''
def get_validated_input(prompt, range):
    try:
        value = int(input(prompt))
        if value not in range:
            raise ValueError
        # return the user input value if valid
        return value
    except ValueError:
        print(f"Enter only numbers in range {range.start} to {range.stop - 1}!")
        exit()

'''
    Check if the theme word is a real english word.
    Return true if real and false if not.
'''
def is_valid_word(theme_word):
    response = requests.get(f"https://api.datamuse.com/words?sp={theme_word}&max=1")
    data = response.json()
    return len(data) > 0 and data[0]['word'].lower() == theme_word.lower()

'''
    Get words related to the user input theme word using Datamuse API
    Return a list of related words
'''
def get_related_words(theme_word, num_words):
    response = requests.get(
        "https://api.datamuse.com/words",
        params={"ml": theme_word, "max": num_words}
    )
    if response.status_code != 200:
        raise Exception(f"Datamuse API error: {response.status_code}")
    
    related_words = [item["word"] for item in response.json()]
    related_words.insert(0, theme_word)
    return related_words

'''
    Gets the meaning and definition of a word
    Uses the Dictionary API, returns a list of meanings
'''
def get_word_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if isinstance(data, list):
            return data[0]['meanings'][0]['definitions'][0]['definition']
        else:
            return "No definition found."
    except Exception as e:
        return "Error fetching definition."

'''# width and height of the figure
width, height = 20, 10'''

'''
    Generate the spiral coord points
    Returns a list of coord points
'''
def gen_spiral_coord(center_x, center_y, num_points, width, height, a=1.5, b=0.08):
    coord = []
    theta = 0
    for _ in range(num_points):
        r = a + b * theta
        x = center_x + r * np.cos(theta)
        y = center_y + r * np.sin(theta)
        if 0 <= x <= width and 0 <= y <= height:
            coord.append((x, y))
        theta += 0.08
    return coord
        
'''# create the spiral coord points
coord = gen_spiral_coord(width / 2, height / 2, 8000)

# total number of coord points
total_coord = len(coord)

# prepare the figure
fig, ax = plt.subplots(figsize=(20, 10))
plt.xlim(0, width)
plt.ylim(0, height)
plt.axis('off')
fm = plt.get_current_fig_manager()
fm.full_screen_toggle()

# debug mode: plot all original coord points as white
if DEBUG_MODE:
    xs, ys = zip(*coord)
    ax.scatter(xs, ys, color='red', s=20)

# track used points
used_coord = []

# track unused points
unused_coord = []

# hold any unused words
unused_words = []

# to store the boundary boxes for detecting overlaps
boxes = []

# to store all the placed words and their bounding boxes
placed_words = []

# R-tree box index
box_index = index.Index()'''

'''
    Close the word cloud figure when the user clicks the esc button
'''
def close_fig(e):
    if e.key == 'escape':
        plt.close(e.canvas.figure)

'''
    Generate the basic word cloud
'''
def basic_word_cloud(word_list, bkg_color, theme_color, other_colors, font_weight, font_type):

    # width and height of the figure
    width, height = 20, 10

    # generate the spiral coord points for this generation
    coord = gen_spiral_coord(width / 2, height / 2, 8000, width, height,)
    total_coord = len(coord)

    # prepare the figure for this generation
    fig, ax = plt.subplots(figsize=(width, height))
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.axis('off')
    fm = plt.get_current_fig_manager()
    fm.full_screen_toggle()
    fig.set_facecolor(bkg_color)  # set background color here

    # debug mode: plot all original coord points as white
    if DEBUG_MODE:
        xs, ys = zip(*coord)
        ax.scatter(xs, ys, color='red', s=20)

    # track used points for this generation
    used_coord = []
    # track unused points for this generation
    unused_coord = []
    # hold any unused words for this generation
    unused_words = []
    # to store the boundary boxes for detecting overlaps for this generation
    boxes = []
    # to store all the placed words for this generation
    placed_words = []
    # r-tree box index for this generation
    box_index = index.Index()
    
    # set background color and connect hover and close effect
    fig.set_facecolor(bkg_color)
    fig.canvas.mpl_connect('motion_notify_event', lambda event: on_hover(event, fig, placed_words))
    fig.canvas.mpl_connect('key_press_event', close_fig)

    # total number of words
    total_words = len(word_list)
    # extract the theme word from word list
    theme_word = word_list.pop(0)

    # split into groups based on lengths
    one_third = total_words // 3
    two_third = one_third * 2
    first = word_list[:one_third]
    second = word_list[one_third:two_third]
    third = word_list[two_third:]

    # track number of placed words
    num_placed_words = 0

    # place the theme word first
    (_, theme_coords, num_placed_words) = place_words(
        [theme_word], (100, 100), font_weight, font_type, theme_color, 
        0, (10, 5), num_placed_words, total_words, coord, boxes, box_index, 
        used_coord, unused_coord, unused_words, fig, ax, placed_words
        )

    # get color ranges
    #color_range = [color1, color2, color3]

    # place the related words
    (unused_points, num_coord, num_placed_words) = place_words(
        first, (20, 35), font_weight, font_type, other_colors, 0, (), num_placed_words, total_words,
        coord, boxes, box_index, used_coord, unused_coord, unused_words, fig, ax, placed_words
        )
    (up2, nc2, num_placed_words) = place_words(
        second, (10, 20), font_weight, font_type, other_colors, 90, (), num_placed_words, total_words,
        coord, boxes, box_index, used_coord, unused_coord, unused_words, fig, ax, placed_words
        )
    (up3, nc3, num_placed_words) = place_words(
        third, (10, 15), font_weight, font_type, other_colors, 0, (), num_placed_words, total_words,
        coord, boxes, box_index, used_coord, unused_coord, unused_words, fig, ax, placed_words
        )
    unused_points += up2 + up3
    num_coord += theme_coords + nc2 + nc3

    # initialize unused words
    unused_words_2 = []

    # initiate the second chance for any unused words
    if unused_words:
        (unused_points_2, unused_words_2) = second_chance(
            unused_words, (7, 10), font_weight, font_type, other_colors, 0,
            coord, boxes, box_index, used_coord, unused_coord, fig, ax, placed_words
            )

    # begin the last chance if still any unused words remaining
    if unused_words_2:
        # get last coord point to try with
        last_coord = coord[num_coord:]
        unused_points_3 = last_chance(
            unused_words_2, last_coord, (7, 10), font_weight, font_type, other_colors, (0, 90),
            boxes, box_index, used_coord, fig, ax, placed_words
            )

    # display accuracy statistics
    if STATISTICS_MODE:
        print(f'(1ST ATTEMPT) - Number of failed coordinate points: {unused_points} / {total_coord}')
        if unused_words:
            print(f'(2ND CHANCE) - Number of failed coordinate points: {unused_points_2} / {total_coord}')
        if unused_words_2:
            print(f'(LAST CHANCE) - Number of failed coordinate points: {unused_points_3} / {total_coord}')

    # display the word cloud
    plt.show()

    # save the figure to a BytesIO buffer
    buffer = BytesIO()
    fig.savefig(buffer, format="PNG", bbox_inches='tight', pad_inches=0)
    buffer.seek(0)
    plt.close(fig) # close figure to free up memory
    return buffer

'''
    Attempt to place all the words on the word cloud
    Returns the total number of unused points, current coord index, and number of placed words
'''
def place_words(
        words, fontrange, fontweight, font_type, color_range, rotation, 
        theme_points, num_placed_words, total_words, coord, boxes, box_index, 
        used_coord, unused_coord, unused_words, fig, ax, placed_words
        ):

    # track the number of unused points
    unused_points = 0
    # keep track of coordinate index
    coord_index = 0
    # get the range for the current words font sizes
    min_size = fontrange[0]
    max_size = fontrange[1]

    # place each word in the current words list
    for word in words:
        # flag for if current word was placed
        placed = False
        x, y = 0, 0 # initialize x and y

        # attempt multiple tries per word, decreasing the font size each time
        for fontsize in range(max_size, min_size - 1, -5):

            # continue until coord is empty
            while coord_index < len(coord):

                # check for theme word placement
                if len(theme_points) > 0:
                    x, y = theme_points
                    color = color_range
                else:
                    x, y = coord[coord_index]
                    # get color for current word
                    color = random.choice(color_range)

                # create the text object with current attributes
                text_obj = plt.text(
                    x, y, word,
                    fontsize=fontsize,
                    fontweight=fontweight,
                    fontfamily=font_type,
                    ha='center', va='center',
                    color=color,
                    rotation=rotation
                )
                fig.canvas.draw() # draw for checking bounds

                # get boundary box in display coords
                box = text_obj.get_window_extent(renderer=fig.canvas.get_renderer())
                # convert to data coords
                box_data = box.transformed(ax.transData.inverted())
                # get padded box
                padded_box = box_data.expanded(1.415, 1.415)
                
                # check for a collision with near text objects
                collisions = list(box_index.intersection(padded_box.extents))
                if not collisions:
                    # add text object (no collision detected)
                    boxes.append(padded_box)
                    box_index.insert(len(boxes) - 1, padded_box.extents)
                    # add used coord points
                    used_coord.append((x, y))
                    placed = True # flip flag
                    # display the padded box surrounding the word
                    if DEBUG_MODE:
                        rect = plt.Rectangle((padded_box.x0, padded_box.y0),
                            padded_box.width, padded_box.height,
                            linewidth=1, edgecolor='red', facecolor='none')
                        ax.add_patch(rect)
                    num_placed_words += 1
                    #os.system('cls')
                    # display words placed in terminal
                    print(f'Words placed: {num_placed_words}/{total_words}')
                    placed_words.append((word, padded_box))
                    break
                else:
                    # remove collision text object
                    text_obj.remove()

                # move to next coord point in coord
                coord_index += 1    
            # break the loop if word is placed
            if placed:
                break

        # if word could not be placed after all decreasing font size attempts
        if not placed:
            #add to unused_words
            unused_words.append(word)
            # increment unused points
            unused_points += 1
            # add unused coord points
            unused_coord.append((x, y))

    return (unused_points, coord_index, num_placed_words)

'''
    The second chance to place any unused words (this time with a smaller font size)
    First tries to place on unused coord points
    Next tries to place with global remaining coord points
    Returns the total number of unused points and unused words after second attempt
'''
def second_chance(
        unused_words, fontrange, fontweight, font_type, color_range, rotation,
        coord, boxes, box_index, used_coord, unused_coord, fig, ax, placed_words       
        ):

    # track the number of unused points
    unused_points = 0
    # track unused words
    unused_words_2 = []
    # get the range for the current words font sizes
    min_size = fontrange[0]
    max_size = fontrange[1]

    # place each word from the unused words list
    for unused_word in unused_words:

        # flag for if current word was placed
        placed = False
        # get the current words font size from the current range
        fontsize = random.randint(min_size, max_size)
        # get random color from color range
        color = random.choice(color_range)

        # continue until unused coord points are empty
        while unused_coord:

            # get a new coordinate
            x, y = unused_coord.pop()
            # create the text object with current attributes
            text_obj = plt.text(
                x, y, unused_word,
                fontsize=fontsize,
                fontweight=fontweight,
                fontfamily=font_type,
                ha='center', va='center',
                color=color,
                rotation=rotation
            )
            fig.canvas.draw() # draw for checking bounds

            # get boundary box in display coords
            box = text_obj.get_window_extent(renderer=fig.canvas.get_renderer())
            # convert to data coords
            box_data = box.transformed(ax.transData.inverted())
            # get padded box
            padded_box = box_data.expanded(1.415, 1.415)
            
            # check for a collision with near text objects
            collisions = list(box_index.intersection(padded_box.extents))
            if not collisions:
                # add text object (no collision detected)
                boxes.append(padded_box)
                box_index.insert(len(boxes) - 1, padded_box.extents)
                # add used coord points
                used_coord.append((x, y))
                placed = True # flip flag
                if DEBUG_MODE:
                    # display the padded box surrounding the word
                    rect = plt.Rectangle((padded_box.x0, padded_box.y0),
                            padded_box.width, padded_box.height,
                            linewidth=1, edgecolor='red', facecolor='none')
                    ax.add_patch(rect)
                # display words placed in terminal
                print(f'Successfully placed {unused_word} on second chance')
                break
            else:
                # remove collision text object
                text_obj.remove()
                # increment unused points
                unused_points += 1

        # add unused word to unused words 2 list
        if not placed:
            unused_words_2.append(unused_word)

    return (unused_points, unused_words_2)

'''
    The last chance attempts to place any words that failed the second chance attempt
    This attempt tries to place each unused word with a much smaller font on all the remaining points
    Keeps iterating until either all words have been placed or all points have been searched
    Returns the number of any unused points that were unable to be placed after this attempt
'''
def last_chance(unused_words_2, last_coord, fontrange, fontweight, font_type, color_range, rotationrange,
                boxes, box_index, used_coord, fig, ax, placed_words
                ):

    # track the number of unused points
    unused_points = 0
    # get the range for the current words font sizes
    min_size = fontrange[0]
    max_size = fontrange[1]
    # get the range for the rotation
    r1 = rotationrange[0]
    r2 = rotationrange[1]
    # randomize the last coordinate points
    random.shuffle(last_coord)

    # place each word in the unused words list
    for unused_word_2 in unused_words_2:

        # get the current words font size from the current range
        fontsize = random.randint(min_size, max_size)
        # get random rotation (either 0 or 90 degrees)
        rotation = random.choice([r1, r2])
        # get random color from color range
        color = random.choice(color_range)

        # continue until coord is empty
        while last_coord:

            # get a new coordinate
            x, y = last_coord.pop()
            # create the text object with current attributes
            text_obj = plt.text(
                x, y, unused_word_2,
                fontsize=fontsize,
                fontweight=fontweight,
                fontfamily=font_type,
                ha='center', va='center',
                color=color,
                rotation=rotation
            )
            fig.canvas.draw() # draw for checking bounds

            # get boundary box in display coords
            box = text_obj.get_window_extent(renderer=fig.canvas.get_renderer())
            # convert to data coords
            box_data = box.transformed(ax.transData.inverted())
            # get padded box
            padded_box = box_data.expanded(1.415, 1.415)
            
            # check for a collision with near text objects
            collisions = list(box_index.intersection(padded_box.extents))
            if not collisions:
                # add text object (no collision detected)
                boxes.append(padded_box)
                box_index.insert(len(boxes) - 1, padded_box.extents)
                # add used coord points
                used_coord.append((x, y))
                if DEBUG_MODE:
                    # display the padded box surrounding the word
                    rect = plt.Rectangle((padded_box.x0, padded_box.y0),
                            padded_box.width, padded_box.height,
                            linewidth=1, edgecolor='red', facecolor='none')
                    ax.add_patch(rect)
                # display words placed in terminal
                print(f'Successfully placed {unused_word_2} on last chance')
                break
            else:
                # remove collision text object
                text_obj.remove()
                # increment unused points
                unused_points += 1

    return unused_points

'''
    Hovered words signal the matplotlib toolbar to output the hovered words definition
'''
def on_hover(event, fig, placed_words):
    if not event.inaxes:
        return
    # get the inverse transform to go from display to data coordinates
    inverse_transform = event.inaxes.transData.inverted()
    mouse_data_x, mouse_data_y = inverse_transform.transform((event.x, event.y))
    # for each word connect to toolbar on hover
    for word, bbox in placed_words:
        if bbox.contains(mouse_data_x, mouse_data_y):
            fig.canvas.toolbar.set_message(f"{word}: {get_word_meaning(word)}")
            return
    # reset toolbar
    fig.canvas.toolbar.set_message("Press ESC to close")