import math
import re

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from nltk.tokenize import RegexpTokenizer
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS

all_stop_list = ['button','love','great', 'product', 'extra',
                 'nice', 'good', 'different', 'perfect', 'thing']
baby_stop_list = ['baby', 'pacifier', 'different', 'pacifiers', 'diaper']
hair_dryer_stop_list = ['overall', 'nice','hair','dryer']
micro_stop_list = ['microwave']

word_tokenizer = RegexpTokenizer("[A-Za-z]+")
file_list = ["microwave", "hair_dryer", "pacifier"]


def usefulness(useful, total):
    z = 1.96
    useful += 1
    total += 1
    p = useful / total
    n = total
    return (p + 1 / (2 * n) * z * z - z * math.sqrt(p * (1 - p)
            / n + z * z / (4 * n * n))) / (1 + 1 / n * z * z)


def pic_generator(file_name):
    feeds = []
    with open(file_name + ".tsv", "r", encoding='utf-8') as f:
        content = f.read().splitlines()[1:]
    for user_info in content:
        user = user_info.split("\t")
        useful_rate = usefulness(int(user[8]), int(user[9]))

        product = user[3]
        review_header = user[12]
        review_body = user[13]
        star = int(user[7])

        vine = 1 if user[10].upper() == "Y" else 0
        verify = 1 if user[11].upper() == "Y" else 0

        if len(re.findall("Star", review_header)) == 0:
            review = review_header + "\n" + review_body
        else:
            review = review_body
        length_r = len(word_tokenizer.tokenize(review))
        length = 1 - 1 / math.exp(length_r / 50)

        polarity, subjectivity = TextBlob(review).sentiment

        value = 0.2852 * useful_rate + 0.0475 * length + 0.0755 * (
                1 - subjectivity) + 0.4210 * vine + 0.1708 * verify

        feeds.append((value, review))

    valuable_feeds = [x[1] for x in feeds if x[0] > 0.5]
    total_feed = ""
    for x in valuable_feeds:
        for y in TextBlob(x).noun_phrases:
            total_feed += y + " "

    text = total_feed

    alice_coloring = np.array(Image.open(file_name + ".png"))

    stopwords = set(STOPWORDS)
    stopwords.add("br")
    stopwords.add("n't")
    for x in all_stop_list:
        stopwords.add(x)

    if file_name == 'pacifier':
        for x in baby_stop_list:
            stopwords.add(x)
    elif file_name == 'hair_dryer':
        for x in hair_dryer_stop_list:
            stopwords.add(x)
    else:
        for x in micro_stop_list:
            stopwords.add(x)
    wc = WordCloud(background_color="white",
                   max_words=2000,
                   mask=alice_coloring,
                   stopwords=stopwords,
                   max_font_size=40,
                   random_state=42, scale=2
                   )
    wc.generate(text)
    plt.figure(figsize=(50, 50))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(file_name + "_cloud.png", format="png")
    plt.show()


if __name__ == '__main__':
    for file in file_list:
        pic_generator(file)