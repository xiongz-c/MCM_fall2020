import re
import numpy as np
from textblob import TextBlob

file_list = ["microwave", "hair_dryer", "pacifier"]
negative_word_list = ['angry', 'bad', 'useless', 'hate']
positive_word_list = ['happy', 'good', 'useful', 'love']


def get_sentence(head, body):
    if "star" in head:
        text = body
    else:
        text = head + "\n" + body
    return text


def file_reader(filename):
    with open(filename, "r", encoding='utf-8') as f:
        items = f.read().splitlines()
        for item in items[1:]:
            yield item


if __name__ == '__main__':
    star_sum, review_sum = {}, {}

    for file in file_list:
        for lines in file_reader(file + ".tsv"):
            info = lines.split('\t')
            star = int(info[7])
            head = info[12]
            body = info[13]
            text = get_sentence(head, body)
            review_score = TextBlob(text).sentiment.polarity
            for target_list in [negative_word_list, positive_word_list]:
                for word in target_list:
                    if re.search(word, text):
                        if word in star_sum:
                            star_sum[word].append(star)
                        else:
                            star_sum[word] = [star]
                        if word in review_sum:
                            review_sum[word].append(review_score)
                        else:
                            review_sum[word] = [review_score]
    avg_star, avg_score = {}, {}
    for key in star_sum.keys():
        avg = np.mean(star_sum[key])
        avg_star[key] = avg
    for key in review_sum.keys():
        avg = np.mean(review_sum[key])
        avg_score[key] = avg
    for key in avg_star.keys():
        print("key_word:%s,avg_star:%.3f,avg_score:%.3f"
              % (key, avg_star[key], avg_score[key]))
