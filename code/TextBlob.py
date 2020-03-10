from textblob import TextBlob


def file_reader(filename):
    with open(filename, "r", encoding='utf-8') as f:
        items = f.read().splitlines()
        for item in items[1:]:
            yield '\n'.join(item.split("\t")[12:14])


def main():
    for text in file_reader("./microwave.tsv"):
        b = TextBlob(text)
        data = [i.sentiment for i in b.sentences]
        print(data)


if __name__ == '__main__':
    main()