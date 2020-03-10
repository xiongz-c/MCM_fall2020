import json
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

file_name = "pacifier"
product_id = "B003CK3LDI"
chart_name = ("Feedback Count", "Length Count")[1]

with open("./" + file_name + ".json", "r") as f:
    content = json.loads(f.read())

product_dict = {}

for con in content:
    if con[0] not in product_dict:
        product_dict[con[0]] = []
    product_dict[con[0]].append({
        "score": con[1],
        "polarity": con[2],
        "star": con[3],
        "date": datetime.strptime(con[4], "%Y-%m-%d"),
        "length": con[5]
    })

for product in product_dict:
    product_dict[product].sort(key=lambda x: x["date"])

time_label = []
star_label = []
length_label = []
review_label = []

month_cnt = 0
sum_star = 0
sum_len = 0

for feed in product_dict[product_id]:
    ym = datetime.strptime(feed["date"].strftime("%Y-%m"),
                           "%Y-%m")

    if ym not in time_label:
        if sum_star != 0:
            star_label.append(sum_star / month_cnt)
            length_label.append(sum_len / month_cnt)
            review_label.append(month_cnt)
        month_cnt = sum_star = 0
        sum_len = 0
        time_label.append(ym)

    month_cnt += 1
    sum_star += feed["star"]
    sum_len += feed["length"]

star_label.append(sum_star / month_cnt)
length_label.append(sum_len / month_cnt)
review_label.append(month_cnt)

fig = plt.figure(figsize=(20, 5))
ax1 = fig.add_subplot()
ax1.plot(time_label, star_label, '.-',
         color=(231 / 255, 76 / 255, 60 / 255))
ax1.set_ylabel('Star Rating')

ax2 = ax1.twinx()
if chart_name == "Feedback Count":
    ax2.bar(time_label, review_label, color="grey", width=15)
elif chart_name == "Length Count":
    ax2.bar(time_label, length_label, color="grey", width=15)
ax2.set_ylabel(chart_name)
plt.xticks(pd.date_range(time_label[0].strftime("%Y-%m-%d"),
                         time_label[-1].strftime("%Y-%m-%d"),
                         freq='1m'))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'))
plt.title(file_name + "(" + product_id + ")")
plt.savefig("./Pics/TimeChart/" + product_id + "_" + chart_name
            + ".eps", format="eps")
plt.show()
