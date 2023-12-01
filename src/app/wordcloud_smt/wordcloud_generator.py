from wordcloud import WordCloud


def wc_generator(content):
    wordcloud_obj = WordCloud(background_color='white')
    wordcloud_obj.generate(content)
    return wordcloud_obj

