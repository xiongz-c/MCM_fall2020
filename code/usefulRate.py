import math

import matplotlib.pyplot as plt
import numpy as np

filename = "hair_dryer"

with open("./" + filename + ".tsv", "r") as f:
    content = f.read().splitlines()[1:]

z = 1.96


def gao(p, n):
    return (p + 1 / (2 * n) * z * z - z *
            math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (
            1 + 1 / n * z * z)


useful_list = []
useless_list = []
for user_info in content:
    user = user_info.split("\t")
    total_vote = int(user[9]) + 1
    useful_vote = int(user[8]) + 1
    ratio = gao(useful_vote / total_vote, total_vote)
    useful_list.append(ratio)
    useless_list.append(1 - ratio)

plt.hist(useful_list, bins=20,
         color=(231 / 255, 76 / 255, 60 / 255),
         label='Usefulness')

plt.xlim((0, 1))
plt.xticks(np.arange(0, 1, 0.05), fontsize=8)

plt.title(filename)
plt.xlabel('Corrected Ratio', fontsize=14)
plt.ylabel('Counts', fontsize=14)
plt.legend(loc='upper right')
plt.savefig("./Pics/useful_ratio_" + filename + "_new.eps",
            format='eps')
plt.show()
