from flask import Flask,render_template
from flask import request
import os
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from string import Template
import traceback

import re


from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd

#load the ml model
from joblib import load
loaded = load('model.joblib')

#plotly
import plotly.graph_objects as go

downloads = 0
app = Flask(__name__)

regex = re.compile('[^a-zA-Z]')
@app.route('/')

def index():
	return render_template("index.html")
@app.route('/', methods = ['POST'])
def process():
	link = request.form['app-link']
	print("Link: " + link)
	rating = scrape(link)
	downloads = get_download_count()
	p = multiprocessing.Process(target=extract)
	p.start()
	#wait for 3 seconds
	p.join(3)

	if p.is_alive():
		print("Force terminate")
		p.terminate()
		p.join()

	merge()	
	predicted_values = predict()
	print(predicted_values.keys())
	try:
		pos = predicted_values['[3]']
	except KeyError:
		pos = 0
	try:
		neg = predicted_values['[1]']
	except KeyError:
		neg = 0
	try:
		neu = predicted_values['[2]']
	except KeyError:
		neu = 0
	total_count = pos + neg + neu
	my_score = (pos * 4.5 + neg * 1.5 + neu * 3 )/total_count 
	print("pos = " + str(pos))
	print("neg = " + str(neg))
	print("neu = " + str(neu))

	print(my_score)
	analytics(predicted_values)

	deviation = abs(float(rating) - my_score)/float(rating) * 100

	return render_template("dashboard.html",var1=downloads,var2=rating,var3=my_score,var4=deviation,piechart="plot.png")

def scrape(link):

	driver = webdriver.Firefox(executable_path='./geckodriver') # initialize driver

	suffix = '&showAllReviews=true'
	driver.get(link + suffix)
	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	match=0	
	while(match < 1):
		#print('In while')
		lastCount = lenOfPage
		time.sleep(2)
		lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		#if lastCount==lenOfPage:
		match=match+1
		if match % 5 == 0:
			#click on show more
			try:
				show_more_list = driver.find_elements_by_xpath("//*[contains(text(), 'Show More')]")
				for show_more in show_more_list:
					show_more.click()
			except:
				traceback.print_exc()
				#print('haga')
	
	element = driver.find_element_by_css_selector("body")
	element.send_keys(Keys.CONTROL+'a')
	element.send_keys(Keys.CONTROL+'c')
	text = pyperclip.paste()

	writer = open('temp_raw','w')
	writer.write(text)
	writer.close()
	
	review_score = driver.find_elements_by_xpath("//div[substring(@aria-label,string-length(@aria-label) -string-length('stars out of five stars') +1) = 'stars out of five stars']")
	score_list = []


	for score in review_score:
	
		desc = score.get_attribute("aria-label")
		#print(desc)
		score_list.append(desc.split(' ')[1])


	playstore_rating = score_list[0]
	#data[playstore_rating] = playstore_rating

	filtered_scores = [score for score in score_list if '.' not in score]
	
	score_writer = open('temp_scores.csv', 'w')
	score_writer.write('ratings\n')
	for score in filtered_scores:
		score_writer.write(score + '\n')
	driver.close()
	return playstore_rating

def process_text(text):
	text = text.encode('ascii', 'ignore').decode('ascii')
	text = regex.sub(' ', text)
	text = text.lower();
	#text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
	# remove special characters and digits
	#text=re.sub("(\\d|\\W)+"," ",text)

	#print(text)
	return text

def get_download_count():
	reader = open('temp_raw', 'r')
	for line in reader:
		line = re.sub('[^0-9a-zA-Z]+', '', line)
		if re.match('[0-9]+', line):
			return line
	return 0

def extract():
	
	reader = open('temp_raw', 'r')
	writer = open('filtered_reviews.csv', 'w')
	writer.write('date, year, likes, reviews' + '\n')
	
	header_complete = False
	counter = 0
	months = set(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August' , 'September' , 'October', 'November', 'December'])
	for line in reader:
		
		if line.strip() == 'Similar':
			break
		if line.strip() == "":
			break
		line = line.strip()
		if(header_complete == False):
			if line == 'User reviews':
				header_complete = True
		else:
			to_write = ''
			line_tokens = line.split(' ')
			while line_tokens[0] not in months:
				line = reader.readline()
				line_tokens = line.split(' ')
			date_line = line.strip()
			count_line = reader.readline().strip()
			if count_line.isnumeric():
				review_line = reader.readline().strip()
				filtered = process_text(review_line)
				to_write = date_line + "," + count_line + "," + filtered + '\n' 
			else:
				
				filtered = process_text(count_line)
				to_write = date_line + "," + "0" + "," + filtered + '\n' 
		
			writer.write(to_write)
	#print("Downloads: " + downloads)
	#data['downloads'] = downloads
	writer.close()
	reader.close()


def merge():
	reader1 = open('filtered_reviews.csv')
	reader2 = open('temp_scores.csv')
	writer = open('app_reviews.csv', 'w')
	for line in reader1:
		to_write = line.strip()+ ',' + reader2.readline()
		writer.write(to_write)
	writer.close()
	reader1.close()
	reader2.close()
def predict():
	global loaded
	reader = open('filtered_reviews.csv')
	pred = {}
	for line in reader:
		raw_text = line.split(',')[-1]
		query = ' '.join(token for token in raw_text.split())
		val = str(loaded['model'].predict([query]))
		#print(val)
		#print("Type of val: " + str(type(val)))
		try:
			pred[val] = pred[val]  + 1
		except KeyError:
			pred[val] = 1

	
	print(pred)
	print('\n\nDone!\n\n')
	return pred

def plot(pred):
	labels = ['Positive', 'Negative', 'Neutral']

	values = []
	positive_count = 0
	negative_count = 0
	neutral_count = 0

	try:
		positive_count = pred['[3]']
	except KeyError:
		positive_count = 0
	try:
		negative_count = pred['[1]']
	except KeyError:
		negative_count = 0
	try:
		neutral_count = pred['[2]']
	except KeyError:
		neutral_count = 0
	values.append(positive_count)
	values.append(negative_count)
	values.append(neutral_count)

	print('Values: '+  str(values))

	colors = ['rgb(0,0,255)' , 'rgb(255,0,0)', 'rgb(255,255,0)']
	figure = go.Figure(data = [go.Pie(labels = labels, values = values, marker_colors = colors, hole = .7)])
	figure.write_image("./static/plot.png")


def analytics(predicted_values):
	#create sentiment pie chart
	#predicted_values = predict()	
	plot(predicted_values)
	
	#create positive, negetive word cloud
	create_word_cloud("positive")	#positive word cloud
	create_word_cloud("negative")	#negative word cloud

	#calculate your rating
	
	#deviation
	
	#if deviation > threshold:
	#	suspicious/skewed ratings
	#else
	#	ratings are valid
	print("placeholder for analytics")

	

def create_word_cloud(mode):
	try:
		df = pd.read_csv('app_reviews.csv', sep='\s*,\s*')
		if mode == "positive":
			df = df.loc[(df.ratings == 4) | (df.ratings == 5)]
		elif mode == "negetive":
			df = df.loc[(df.ratings == 1) | (df.ratings == 2)]
		word_dump = ''
		for line in df['reviews']:
			word_dump = word_dump+' '.join(token for token in str(line).split() if token not in STOPWORDS)
		#print(word_dump)

		wordcloud = WordCloud(width=600, height=600,background_color ='white',	stopwords = STOPWORDS, min_font_size = 10).generate(word_dump) 

		# plot the WordCloud image					 
		fig = plt.figure(figsize = (8, 8), facecolor = None) 
		plt.imshow(wordcloud) 
		plt.axis("off") 
		plt.tight_layout(pad = 0) 
		#plt.show() 

		print("\n\n Worked till here! \n\n")
		if mode == "positive":
			fig.savefig("pos.png")
		elif mode == "negative":
			fig.savefig("neg.png")
		else:
			fig.savefig("cust.png")
	except:
		traceback.print_exc()	
if __name__ == "__main__":
	app.run(debug=True)
