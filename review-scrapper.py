from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from string import Template
import traceback
driver = webdriver.Firefox(executable_path='./geckodriver') # initialize driver


curr = 7
reader = open('app_ids', 'r')
link_stub = Template('https://play.google.com/store/apps/details?id=$appid&showAllReviews=true')
for line in reader:
	app_id = line
	app_url = link_stub.substitute(appid = app_id)	
	#print("App url: " + app_url)
	driver.get(app_url)
	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	match=0	
	while(match < 3):
		#print('In while')
		lastCount = lenOfPage
		time.sleep(2)
		lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		#if lastCount==lenOfPage:
		match=match+1
		if match % 5 == 0:
			#click on show more
			try:
				#show_more = driver.find_elements_by_class_name("ZFr60d CeoRYc")[0]
				#show_more.click()
				show_more_list = driver.find_elements_by_xpath("//*[contains(text(), 'Show More')]")
				for show_more in show_more_list:
					show_more.click()
			except:
				traceback.print_exc()
		
	element = driver.find_element_by_css_selector("body")
	element.send_keys(Keys.CONTROL+'a')
	element.send_keys(Keys.CONTROL+'c')
	text = pyperclip.paste()

	writer = open('./review_dump/'+str(curr),'w')
	writer.write(text)
	writer.close()

	count = 1
	#search_query_stub = 'stars out of five stars'
	#review_score = driver.find_elements_by_xpath("//*[contains(text(), 'stars out of five stars')]")

	#review_score driver.find_elements_by_xpath('//div[@aria-label="Rated 3 stars out of five stars"]')
	#aria-label	

	#driver.find_elements_by_xpath("//*[ends-with(@aria-label,'stars out of five stars')]")
	review_score = driver.find_elements_by_xpath("//div[substring(@aria-label,string-length(@aria-label) -string-length('stars out of five stars') +1) = 'stars out of five stars']")
	score_list = []
	
	
	for score in review_score:
		
		desc = score.get_attribute("aria-label")
		#print(desc)
		score_list.append(desc.split(' ')[1])

	#print(score_list)
	playstore_rating = score_list[0]
	
	filtered_scores = [score for score in score_list if '.' not in score]
	#print(filtered_scores)
	
	score_writer = open('./review_filtered/' + str(curr) + '_scores.csv', 'w')
	for score in filtered_scores:
		score_writer.write(score + '\n')
	#driver.close()
	print("Completed mining: " + str(curr))
	curr = curr+1
