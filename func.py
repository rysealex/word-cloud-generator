from wordcloud import WordCloud
from rtree import index
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import random
import requests
import os

'''
    -------------------------------------------------------------------------------------------------------
                                            Basic word cloud generator
    -------------------------------------------------------------------------------------------------------
'''

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
    Width, height, and step constants
'''

# width and heigth of figure
width, height = 20, 10
# spacing between points
step = 0.5

'''
    Generate the spiral coord points
    Returns a list of coord points
'''
def gen_spiral_coord(center_x, center_y, num_points, a=1.5, b=0.08):
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
        
# create the spiral coord points
coord = gen_spiral_coord(width / 2, height / 2, 8000)

# shuffle the coord points
#random.shuffle(coord)

# total number of coord points
total_coord = len(coord)

# prepare the figure
#plt.rcParams['toolbar'] = 'None'
fig, ax = plt.subplots(figsize=(20, 10))
plt.xlim(0, width)
plt.ylim(0, height)
plt.axis('off')
fm = plt.get_current_fig_manager()
fm.full_screen_toggle()

'''# plot all original coord points as white
xs, ys = zip(*coord)
ax.scatter(xs, ys, color='white', s=20)'''

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
box_index = index.Index()

'''
    Generate the basic word cloud
'''
def basic_word_cloud(word_list, bkg_color, theme_color, color1, color2, color3, font_weight, font_type):
    
    # set background color and connect hover effect
    fig.set_facecolor(bkg_color)
    fig.canvas.mpl_connect('motion_notify_event', on_hover)

    # total number of words
    total_words = len(word_list)
    # extract the theme word from word list
    theme_word = word_list.pop(0)
    # sort word list by longest to shortest
    #word_list.sort(key=len, reverse=True)
    #word_list = [theme_word] + word_list
    one_third = total_words // 3
    two_third = one_third * 2
    # split into groups based on lengths
    first = word_list[:one_third]
    second = word_list[one_third:two_third]
    third = word_list[two_third:]

    # track number of placed words
    num_placed_words = 0

    # place the theme word first
    (_, theme_coords, num_placed_words) = place_words(
        [theme_word], (100, 100), font_weight, font_type, theme_color, 
        0, (10, 5), num_placed_words, total_words
        )

    # get color ranges
    color_range = [color1, color2, color3]

    # place the related words
    (unused_points, num_coord, num_placed_words) = place_words(
        first, (20, 35), font_weight, font_type, color_range, 0, (), num_placed_words, total_words
        )
    (up2, nc2, num_placed_words) = place_words(
        second, (10, 20), font_weight, font_type, color_range, 90, (), num_placed_words, total_words
        )
    (up3, nc3, num_placed_words) = place_words(
        third, (10, 15), font_weight, font_type, color_range, 0, (), num_placed_words, total_words
        )
    unused_points += up2 + up3
    num_coord += theme_coords + nc2 + nc3

    # initialize unused words
    unused_words_2 = []

    # initiate the second chance for any unused words
    if unused_words:
        #print("Starting 2ND CHANCE")
        (unused_points_2, unused_words_2) = second_chance(
            unused_words, (7, 10), font_weight, font_type, color_range, 0
            )

    # begin the last chance if still any unused words remaining
    if unused_words_2:
        # get last coord point to try with
        last_coord = coord[num_coord:]
        #print("LAST CHANCE MECHANISM ENGAGED")
        unused_points_3 = last_chance(
            unused_words_2, last_coord, (10, 15), font_weight, font_type, color_range, (0, 90)
            )

    '''# display accuracy
    print(f'(1ST ATTEMPT) - Number of failed coordinates after first attempt: {unused_points} / {total_coord}')
    if unused_words:
        print(f'(2ND CHANCE) - Number of failed coordinates after second attempt: {unused_points_2} / {total_coord}')
    if unused_words_2:
        print(f'(LAST CHANCE) - Number of failed coordinates after last attempt: {unused_points_3} / {total_coord}')
    '''
    plt.show()

'''
    Attempt to place all the words on the word cloud
    Returns the total number of unused points
'''
def place_words(
        words, fontrange, fontweight, font_type, color_range, rotation, 
        theme_points, num_placed_words, total_words
        ):

    # track the number of unused points
    unused_points = 0

    ''' 
    # inflate boundary padding
    padding = 0.1
    '''

    # get the range for the current words font sizes
    min_size = fontrange[0]
    max_size = fontrange[1]

    # keep track of coordinate index
    coord_index = 0

    # padding of box size
    padding_scale = 0.01

    # place each word in the current words list
    for word in words:
        # flag for if current word was placed
        placed = False

        # get the current words font size from the current range
        #fontsize = random.randint(min_size, max_size)

        '''# check for very first word
        if i == 0:
            
            # start at center of image
            x, y = (10, 5)
            # create the text object with current attributes
            text_obj = plt.text(
                x, y, word,
                fontsize=first_size,
                fontweight=fontweight,
                ha='center', va='center',
                color=first_color,
                rotation=rotation
            )
            fig.canvas.draw() # draw for checking bounds

            # get boundary box in display coords
            box = text_obj.get_window_extent(renderer=fig.canvas.get_renderer())
            # convert to data coords
            box_data = box.transformed(ax.transData.inverted())

            # padding of box size
            padding_scale = 0.05

            # get original extents
            x0, y0, x1, y1 = box_data.extents
            width = x1 - x0
            height = y1 - y0

            # apply the padding based on the size of the box
            pad_x = width * padding_scale
            pad_y = height * padding_scale

            # create the padded box
            padded_box = mtransforms.Bbox.from_extents(
                x0 - pad_x, y0 - pad_y, x1 + pad_x, y1 + pad_y    
            )
            padded_box = box_data.expanded(1, 1)
            
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
                rect = plt.Rectangle((padded_box.x0, padded_box.y0),
                     padded_box.width, padded_box.height,
                     linewidth=1, edgecolor='white', facecolor='none')
                ax.add_patch(rect)
                print(f'Successfully placed FIRST word {word}')
                placed_words.append((word, padded_box))
                continue
            else:
                # remove collision text object
                text_obj.remove()
                # increment unused points
                unused_points += 1
                # add unused coord points
                unused_coord.append((x, y))
                continue'''

        # attempt multiple tries per word, decreasing the font size each time
        for fontsize in range(max_size, min_size - 1, -5):

            # continue until coord is empty
            #while coord:
            while coord_index < len(coord):

                # check for theme word placement
                if len(theme_points) > 0:
                    x, y = theme_points
                    color = color_range
                else:
                    x, y = coord[coord_index]
                    # get color for current word
                    color = random.choice(color_range)

                # get a new coordinate
                #x, y = coord[coord_index]
                #print(x, y)
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

                '''
                # inflate boundary box
                x0, y0, x1, y1 = box_data.extents
                inflated_box = mtransforms.Bbox.from_extents(x0 - padding, y0 - padding, x1 + padding, y1 + padding)
                '''

                # get original extents
                x0, y0, x1, y1 = box_data.extents
                width = x1 - x0
                height = y1 - y0

                # apply the padding based on the size of the box
                pad_x = width * padding_scale
                pad_y = height * padding_scale

                # create the padded box
                padded_box = mtransforms.Bbox.from_extents(
                    x0 - pad_x, y0 - pad_y, x1 + pad_x, y1 + pad_y    
                )
                padded_box = box_data.expanded(1.3, 1.3)
                
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
                    '''rect = plt.Rectangle((padded_box.x0, padded_box.y0),
                        padded_box.width, padded_box.height,
                        linewidth=1, edgecolor='white', facecolor='none')
                    ax.add_patch(rect)'''
                    num_placed_words += 1
                    os.system('cls')
                    print(f'Words placed: {num_placed_words}/{total_words}')
                    placed_words.append((word, padded_box))
                    break
                else:
                    # remove collision text object
                    text_obj.remove()
                    
                coord_index += 1
            if placed:
                break

        # if word could not be placed after all decreasing font size attempts, add to unused_words
        if not placed:
            unused_words.append(word)
            # increment unused points
            unused_points += 1
            # add unused coord points
            unused_coord.append((x, y))
            print(f'Could not place {word}')

    return (unused_points, coord_index, num_placed_words)

'''
    The second chance to place any unused words (this time with a smaller font size)
    First tries to place on unused coord points
    Next tries to place with global remaining coord points
    Returns the total number of unused points
'''
def second_chance(unused_words, fontrange, fontweight, font_type, color_range, rotation):

    # track the number of unused points
    unused_points = 0

    # track unused words
    unused_words_2 = []

    # set the padding scale
    padding_scale = 0.01

    # get the range for the current words font sizes
    min_size = fontrange[0]
    max_size = fontrange[1]

    # place each word in the unused words list
    for unused_word in unused_words:
        # flag for if current word was placed
        placed = False

        # get the current words font size from the current range
        fontsize = random.randint(min_size, max_size)

        # get random color from color range
        color = random.choice(color_range)

        # continue until coord is empty
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

            '''
            # inflate boundary box
            x0, y0, x1, y1 = box_data.extents
            inflated_box = mtransforms.Bbox.from_extents(x0 - padding, y0 - padding, x1 + padding, y1 + padding)
            '''

            # get original extents
            x0, y0, x1, y1 = box_data.extents
            width = x1 - x0
            height = y1 - y0

            # apply the padding based on the size of the box
            pad_x = width * padding_scale
            pad_y = height * padding_scale

            # create the padded box
            padded_box = mtransforms.Bbox.from_extents(
                x0 - pad_x, y0 - pad_y, x1 + pad_x, y1 + pad_y    
            )
            padded_box = box_data.expanded(1, 1)
            
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
                '''rect = plt.Rectangle((padded_box.x0, padded_box.y0),
                        padded_box.width, padded_box.height,
                        linewidth=1, edgecolor='white', facecolor='none')
                ax.add_patch(rect)'''
                print(f'Successfully placed {unused_word} on second chance')
                placed_words.append((unused_word, padded_box))
                break
            else:
                # remove collision text object
                text_obj.remove()
                # increment unused points
                unused_points += 1

        if not placed:
            unused_words_2.append(unused_word)
            print(f'Could not place {unused_word} on unused point')

    return (unused_points, unused_words_2)

def last_chance(unused_words_2, last_coord, fontrange, fontweight, font_type, color_range, rotationrange):

    # track the number of unused points
    unused_points = 0

    # set the padding scale
    padding_scale = 0.05

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
        # flag for if current word was placed
        placed = False

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

            '''
            # inflate boundary box
            x0, y0, x1, y1 = box_data.extents
            inflated_box = mtransforms.Bbox.from_extents(x0 - padding, y0 - padding, x1 + padding, y1 + padding)
            '''

            # get original extents
            x0, y0, x1, y1 = box_data.extents
            width = x1 - x0
            height = y1 - y0

            # apply the padding based on the size of the box
            pad_x = width * padding_scale
            pad_y = height * padding_scale

            # create the padded box
            padded_box = mtransforms.Bbox.from_extents(
                x0 - pad_x, y0 - pad_y, x1 + pad_x, y1 + pad_y    
            )
            padded_box = box_data.expanded(1, 1)
            
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
                '''rect = plt.Rectangle((padded_box.x0, padded_box.y0),
                        padded_box.width, padded_box.height,
                        linewidth=1, edgecolor='white', facecolor='none')
                ax.add_patch(rect)'''
                print(f'Successfully placed {unused_word_2} on last chance')
                placed_words.append((unused_word_2, padded_box))
                break
            else:
                # remove collision text object
                text_obj.remove()
                # increment unused points
                unused_points += 1

        if not placed:
            print(f'Could not place {unused_word_2} on last try')

    return unused_points

def on_hover(event):
    if not event.inaxes:
        return
    # get the inverse transform to go from display to data coordinates
    inverse_transform = event.inaxes.transData.inverted()
    mouse_data_x, mouse_data_y = inverse_transform.transform((event.x, event.y))
    # for each word connect to toolbar on hover
    for word, bbox in placed_words:
        if bbox.contains(mouse_data_x, mouse_data_y):
            fig.canvas.toolbar.set_message(f"Hovered: {word}")
            return
    # rest toolbar
    fig.canvas.toolbar.set_message("")