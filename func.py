from wordcloud import WordCloud
from rtree import index
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import random

'''
    -------------------------------------------------------------------------------------------------------
                                            Advanced word cloud generator
    -------------------------------------------------------------------------------------------------------
'''

'''
    Generates the advanced word cloud
    Saves as png file (wordcloud.png)
'''
def gen_word_cloud(word_list):
    
    text = ' '.join(word_list)

    # create word cloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # save the file
    wordcloud.to_file('wordcloud.png')

'''
    Read words from text file (wordfile.txt)
    Returns word_list, a list of all words
'''
def read_wordfile():

    word_list = []

    # extract words from wordfile
    with open('wordfile.txt', 'r') as file:
        # read each line
        for line in file:
            # read each word
            for word in line.split():
                word_list.append(word)

    return word_list

'''
    -------------------------------------------------------------------------------------------------------
                                            Basic word cloud generator
    -------------------------------------------------------------------------------------------------------
'''

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
def gen_spiral_coord(center_x, center_y, num_points, a=0.5, b=0.05):
    coord = []
    theta = 0
    for _ in range(num_points):
        r = a + b * theta
        x = center_x + r * np.cos(theta)
        y = center_y + r * np.sin(theta)
        if 0 <= x <= width and 0 <= y <= height:
            coord.append((x, y))
        theta += 0.03
    return coord
        
# create the spiral coord points
coord = gen_spiral_coord(width / 2, height / 2, 8000)

# shuffle the coord points
random.shuffle(coord)

# total number of coord points
total_coord = len(coord)

# prepare the figure
fig, ax = plt.subplots(figsize=(22, 11))
plt.xlim(0, width)
plt.ylim(0, height)
plt.axis('off')
fig.set_facecolor('black')

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

# R-tree box index
box_index = index.Index()

'''
    Generate the basic word cloud
'''
def basic_word_cloud(word_list):

    # sort word list by longest to shortest
    word_list.sort(key=len, reverse=True)
    one_third = len(word_list) // 3
    two_third = one_third * 2
    # split into groups based on lengths
    first = word_list[:one_third]
    second = word_list[one_third:two_third]
    third = word_list[two_third:]

    # place the words
    (unused_points, num_coord) = place_words(first, (20, 30), 'bold', '#003366', 0)
    (up2, nc2) = place_words(second, (15, 25), 'bold', '#ff7f0e', 90)
    (up3, nc3) = place_words(third, (10, 25), 'bold', 'yellow', 0)
    unused_points += up2 + up3
    num_coord += nc2 + nc3

    # initiate the second chance for any unused words
    if unused_words:
        print("Starting 2ND CHANCE")
        (unused_points_2, unused_words_2) = second_chance(unused_words, (7, 10), 'bold', '#0770bb', 0)

    # begin the last chance if still any unused words remaining
    if unused_words_2:
        # get last coord point to try with
        last_coord = coord[num_coord:]
        print("LAST CHANCE MECHANISM ENGAGED")
        unused_points_3 = last_chance(unused_words_2, last_coord, (15, 25), 'bold', 'white', (0, 90))

    # display accuracy
    print(f'(1ST ATTEMPT) - Number of failed coordinates after first attempt: {unused_points} / {total_coord}')
    if unused_words:
        print(f'(2ND CHANCE) - Number of failed coordinates after second attempt: {unused_points_2} / {total_coord}')
    if unused_words_2:
        print(f'(LAST CHANCE) - Number of failed coordinates after last attempt: {unused_points_3} / {total_coord}')

    plt.show()

'''
    Attempt to place all the words on the word cloud
    Returns the total number of unused points
'''
def place_words(words, fontrange, fontweight, color, rotation, first_size=60, first_color='red'):

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

    # place each word in the current words list
    for i, word in enumerate(words):
        # flag for if current word was placed
        placed = False

        # get the current words font size from the current range
        #fontsize = random.randint(min_size, max_size)

        # check for very first word
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
            padding_scale = 0.25

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
            padded_box = box_data.expanded(1.75, 1.75)
            
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
                continue
            else:
                # remove collision text object
                text_obj.remove()
                # increment unused points
                unused_points += 1
                # add unused coord points
                unused_coord.append((x, y))
                continue

        # attempt multiple tries per word, decreasing the font size each time
        for fontsize in range(max_size, min_size - 1, -5):

            # continue until coord is empty
            #while coord:

                # get a new coordinate
                x, y = coord[coord_index]
                #print(x, y)
                # create the text object with current attributes
                text_obj = plt.text(
                    x, y, word,
                    fontsize=fontsize,
                    fontweight=fontweight,
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

                # padding of box size
                padding_scale = 0.25

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
                padded_box = box_data.expanded(1.75, 1.75)
                
                '''
                    NEED TO FIX --- COLLISION IS BEING DETECTED FOR EVERY WORD
                '''
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
                    print(f'Successfully placed {word}')
                    break
                else:
                    # remove collision text object
                    text_obj.remove()
                    coord_index += 1
                       
        # if word could not be placed after all decreasing font size attempts, add to unused_words
        if not placed:
            unused_words.append(word)
            # increment unused points
            unused_points += 1
            # add unused coord points
            unused_coord.append((x, y))
            print(f'Could not place {word}')

    return (unused_points, coord_index)

'''
    The second chance to place any unused words (this time with a smaller font size)
    First tries to place on unused coord points
    Next tries to place with global remaining coord points
    Returns the total number of unused points
'''
def second_chance(unused_words, fontrange, fontweight, color, rotation):

    # track the number of unused points
    unused_points = 0

    # track unused words
    unused_words_2 = []

    # get the range for the current words font sizes
    min_size = fontrange[0]
    max_size = fontrange[1]

    # place each word in the unused words list
    for unused_word in unused_words:
        # flag for if current word was placed
        placed = False

        # get the current words font size from the current range
        fontsize = random.randint(min_size, max_size)

        # continue until coord is empty
        while unused_coord:

            # get a new coordinate
            x, y = unused_coord.pop()
            # create the text object with current attributes
            text_obj = plt.text(
                x, y, unused_word,
                fontsize=fontsize,
                fontweight=fontweight,
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

            # set the padding scale
            padding_scale = 0.25

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
                print(f'Successfully placed {unused_word}')
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

def last_chance(unused_words_2, last_coord, fontrange, fontweight, color, rotationrange):

    # track the number of unused points
    unused_points = 0

    # get the range for the current words font sizes
    min_size = fontrange[0]
    max_size = fontrange[1]

    # get the range for the rotation
    r1 = rotationrange[0]
    r2 = rotationrange[1]

    # place each word in the unused words list
    for unused_word_2 in unused_words_2:
        # flag for if current word was placed
        placed = False

        # get the current words font size from the current range
        fontsize = random.randint(min_size, max_size)

        # get random rotation (either 0 or 90 degrees)
        rotation = random.choice([r1, r2])

        # continue until coord is empty
        while last_coord:

            # get a new coordinate
            x, y = last_coord.pop()
            # create the text object with current attributes
            text_obj = plt.text(
                x, y, unused_word_2,
                fontsize=fontsize,
                fontweight=fontweight,
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

            # set the padding scale
            padding_scale = 0.25

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
                print(f'Successfully placed {unused_word_2}')
                break
            else:
                # remove collision text object
                text_obj.remove()
                # increment unused points
                unused_points += 1

        if not placed:
            print(f'Could not place {unused_word_2} on last try')

    return unused_points