import requests
from datetime import datetime
import traceback
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import investpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

plt.rcParams['axes.facecolor'] = '#FFF2E5'
mpl.rcParams['axes.spines.left'] = True
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.bottom'] = True
mpl.rcParams['axes.linewidth'] = 2


analyser = SentimentIntensityAnalyzer()
scores =[]
scores_pos = 0
scores_neg = 0

#url = "https://api.pushshift.io/reddit/{}/search/?q=elon&limit=1000&sort=desc&author={}&before="
rating = []
epoch = 1556668800
for i in range(0,52):
	text_ls = []
	print(epoch, i)
	url_ = f"https://api.pushshift.io/reddit/comment/search/?q=elon+musk&before={str(epoch)}&limit=1000"
	json_ = requests.get(url=url_).json()
	objects = json_['data']
	for object in objects:
		try:
			text = object['body']
			textASCII = text.encode(encoding='ascii', errors='ignore').decode()
			text_ls.append(textASCII)
		except Exception as err:
			print(f"Couldn't print comment")
			print(traceback.format_exc())
	for sentence in text_ls:
		score = analyser.polarity_scores(sentence)
		scores.append(score['compound'])
	avg_score = pd.Series(scores)
	avg_score = avg_score.replace(0, np.nan)
	avg_score = pd.Series(scores).dropna()
	avg_score = avg_score.mean()
	print(round(avg_score,3))
	rating.append(round(avg_score,3))
	epoch = int(epoch)
	epoch += 669600

print(len(rating))

plt.plot(rating,linewidth=2,alpha=0.7,color='#202020')
plt.savefig('musk_reddit_all.png', bbox_inches='tight',dpi=300)
plt.show()