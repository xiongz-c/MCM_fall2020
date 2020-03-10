from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer

file_list = ["microwave", "hair_dryer", "pacifier"]


def file_reader(filename):
    with open(filename, "r", encoding='utf-8') as f:
        items = f.read().splitlines()
        for item in items[1:]:
            yield item


def get_words_len(sentence):
    word_tokenizer = RegexpTokenizer('[A-Za-z]+')
    terms = word_tokenizer.tokenize(sentence)
    return len(terms)


def main():
    for f in file_list:
        with open("new_" + f + ".csv", 'a', encoding='utf-8') as new_f:
            new_f.write('customer_id,review_id,product_id,star_rating,'
                        'vote_ratio,helpful_vote,vine,verified_purchase,'
                        'review_len,review_polarity,review_subjectivity,date\n')
        for lines in file_reader(f + ".tsv"):
            info = lines.split('\t')
            r_headline = info[12]
            if "star" in r_headline:
                text = info[13]
            else:
                text = info[12] + "\n" + info[13]
            result = TextBlob(text).sentiment
            vote_rate = (float(info[8])+1) / (float(info[9])+1)
            if info[10] == "Y" or info[10] == "y":
                vine = 1
            else:
                vine = 0
            if info[11] == "Y" or info[11] == "y":
                purchase = 1
            else:
                purchase = 0
            dic = {"customer_id": info[1], "review_id": info[2],
                   "product_id": info[3], "star_rating": info[7],
                   "vote_ratio": str(vote_rate), "helpful_vote": int(info[8])+1,
                   "vine": vine, "verified_purchase": purchase,
                   "review_len": get_words_len(text),
                   "review_polarity": result.polarity,
                   "review_subjectivity": result.subjectivity, "date": info[14]}
            print_str = list(dic.values())[0]
            for i in range(1, len(dic.values())):
                print_str += ("," + str(list(dic.values())[i]))
            with open("new_" + f + ".csv", 'a', encoding='utf-8') as new_f:
                new_f.write(print_str + '\n')


if __name__ == '__main__':
    main()
