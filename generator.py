from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random

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

    plt.figure(figsize=(10, 5))

    # place all words in first
    for word in first:
        
        x, y = coord.pop()
        plt.text(x, y, word, fontsize=100, fontweight='bold', ha='center', va='center', color='red')

    # place all words in second
    for word in second:
        
        x, y = coord.pop()
        plt.text(x, y, word, fontsize=50, rotation=90, fontweight='bold', ha='center', va='center', color='black')

    # place all words in third
    for word in third:
        
        x, y = coord.pop()
        plt.text(x, y, word, fontsize=25, ha='center', va='center', color='blue')
    
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.axis('off')
    plt.show()

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
STATIC = True

if STATIC:
    word_list = ['Alex', 'Jay', 'Bob', 'Computer', 'Python', 'Java', 'C#', 'CPU', 'Jacob']
else:
    word_list = read_wordfile()

# switch between basic and advanced word cloud generators
BASIC = True  

if BASIC:
    basic_word_cloud(word_list)
else:
    gen_word_cloud(word_list)