from wordcloud import WordCloud
import matplotlib.pyplot as plt

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

# testing here
word_list = ['Alex', 'Jay', 'Bob', 'Computer', 'Python', 'Java']
gen_word_cloud(word_list)