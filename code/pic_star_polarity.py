import pandas as pd
import matplotlib.pyplot as plt

file_list = ["new_microwave.csv", "new_hair_dryer.csv", "new_pacifier.csv"]

if __name__ == '__main__':
    row_list = []
    for file in file_list:
        df = pd.read_csv(file, index_col=11)
        fig = plt.figure()
        plt.scatter(x=df["review_polarity"], y=df["star_rating"], marker='.', c=[[231 / 255, 76 / 255, 60 / 255]])
        plt.xlabel("review_polarity")
        plt.ylabel("star_rating")
        plt.show()
        fig.savefig(file[:-4]+'_polarity.eps', format='eps')
        fig = plt.figure()
        plt.scatter(x=df["review_subjectivity"], y=df["star_rating"], marker='.', c=[[231 / 255, 76 / 255, 60 / 255]])
        plt.xlabel("review_subjectivity")
        plt.ylabel("star_rating")
        plt.show()
        fig.savefig(file[:-4]+'_subjectivity.eps', format='eps')
