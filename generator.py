from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import random

'''
    initializing the figure here
    creating and randomizing all coordinates
    initalizing the boundary boxes for collision detection
'''

# width and heigth of figure
width, height = 18, 9
# spacing between points
step = 1

# generate all possible coordinates
coord = []
for x in range(0, width, step):
    for y in range(0, height, step):
        coord.append((x, y))

# total number of coord points
total_coord = len(coord)

# shuffle the coord
random.shuffle(coord)

# prepare the figure
fig, ax = plt.subplots(figsize=(20, 10))
plt.xlim(0, width)
plt.ylim(0, height)
plt.axis('off')

# plot all original coord points as gray
xs, ys = zip(*coord)
ax.scatter(xs, ys, color='gray', s=20)

# track used points
used_coord = []

# to store the boundary boxes for detecting overlaps
boxes = []

# generate the word cloud
def gen_word_cloud(word_list):
    
    text = ' '.join(word_list)

    # create word cloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # save the fale
    #wordcloud.to_file('wordcloud.png')

def basic_word_cloud(word_list):

    word_list.sort(key=len)
    one_third = len(word_list) // 3
    two_third = one_third * 2
    # split into groups based on lengths
    first = word_list[:one_third]
    second = word_list[one_third:two_third]
    third = word_list[two_third:]

    # place the words
    unused_points = place_words(first, 100, 'bold', 'red', 0)
    unused_points = unused_points + place_words(second, 50, 'bold', 'black', 90)
    unused_points = unused_points + place_words(third, 25, 'normal', 'blue', 0)

    # plot used points as green
    if used_coord:
        xs_used, ys_used = zip(*used_coord)
        ax.scatter(xs_used, ys_used, color='green', s=20)

    '''
    # width and heigth of figure
    width, height = 10, 5
    # spacing between points
    step = 1

    # generate all possible coordinates
    coord = []
    for x in range(0, width, step):
        for y in range(0, height, step):
            coord.append((x, y))

    # shuffle the coord
    random.shuffle(coord)

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.axis('off')

    # store the boundary boxes for detecting overlaps
    boxes = []
    '''

    '''
    # place all words in first
    for word in first:
        
        while coord:
            x, y = coord.pop()
            text_obj = plt.text(x, y, word, fontsize=100, fontweight='bold', ha='center', va='center', color='red')
            fig.canvas.draw()

            box = text_obj.get_window_extent(renderer=fig.canvas.get_renderer())

            box_data = box.transformed(ax.transData.inverted())

            overlaps = any(box_data.overlaps(existing) for existing in boxes)

            if not overlaps:
                boxes.append(box_data)
                break
            else:
                text_obj.remove()

    # place all words in second
    for word in second:
        
        while coord:
            x, y = coord.pop()
            text_obj = plt.text(x, y, word, fontsize=50, rotation=90, fontweight='bold', ha='center', va='center', color='black')
            fig.canvas.draw()

            box = text_obj.get_window_extent(renderer=fig.canvas.get_renderer())

            box_data = box.transformed(ax.transData.inverted())

            overlaps = any(box_data.overlaps(existing) for existing in boxes)

            if not overlaps:
                boxes.append(box_data)
                break
            else:
                text_obj.remove()

    # place all words in third
    for word in third:
        
        while coord:
            x, y = coord.pop()
            text_obj = plt.text(x, y, word, fontsize=25, ha='center', va='center', color='blue')
            fig.canvas.draw()

            box = text_obj.get_window_extent(renderer=fig.canvas.get_renderer())

            box_data = box.transformed(ax.transData.inverted())

            overlaps = any(box_data.overlaps(existing) for existing in boxes)

            if not overlaps:
                boxes.append(box_data)
                break
            else:
                text_obj.remove()
    '''
    
    print(f'The number of unused points: {unused_points} / {total_coord}')
    plt.show()

def place_words(words, fontsize, fontweight, color, rotation):

    # track the number of unused points
    unused_points = 0

    # inflate boundary padding
    padding = 1

    # place each word in the current words list
    for word in words:
        # flag for if current word was placed
        placed = False

        # continue until coord is empty
        while coord:

            # get a new coordinate
            x, y = coord.pop()
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

            # inflate boundary box
            x0, y0, x1, y1 = box_data.extents
            inflated_box = mtransforms.Bbox.from_extents(x0 - padding, y0 - padding, x1 + padding, y1 + padding)

            # check for a collision with near text objects
            if not any(inflated_box.overlaps(existing) for existing in boxes):
                # add text object (no collision detected)
                boxes.append(inflated_box)
                # add used coord points
                used_coord.append((x, y))
                placed = True # flip flag
                break
            else:
                # remove collision text object
                text_obj.remove()
                # increment unused points
                unused_points = unused_points + 1

        if not placed:
            print(f'Could not place {word}')

    return unused_points

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

# switch between static word_list or dynamic word_list from the wordfile.txt
STATIC = False

if STATIC:
    word_list = [
                    'Alex', 'Jay', 'AI', 'Computer', 'Python', 'Java', 'C#', 'CPU', 'Jacob', 'Model', 'Network', 'Code', 
                    'System', 'React', 'JS', 'RAM', 'SQL', 'Algorithms', 'Database', 'Tech', 'Internet', 'Protocol',
                    'Binary', 'Data', 'Software', 'Storage', 'Theory', 'Access', 'Web', 'Security', 'User', 'Virtual'
                    ]
else:
    word_list = read_wordfile()

# switch between basic and advanced word cloud generators
BASIC = True

if BASIC:
    basic_word_cloud(word_list)
else:
    gen_word_cloud(word_list)