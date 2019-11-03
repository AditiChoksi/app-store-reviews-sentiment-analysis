from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from string import Template
import traceback
driver = webdriver.Firefox(executable_path='./geckodriver') # initialize driver


curr = 1
#reader = open('app.names', 'r')
#link_stub = Template('https://play.google.com/store/apps/details?id=$appid&showAllReviews=true')

#lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

#links = ["https://play.google.com/store/apps/collection/cluster?clp=CiMKIQobdG9wc2VsbGluZ19mcmVlX0FQUExJQ0FUSU9OEAcYAw%3D%3D:S:ANO1ljKtW7s&gsr=CiUKIwohCht0b3BzZWxsaW5nX2ZyZWVfQVBQTElDQVRJT04QBxgD:S:ANO1ljL_-aM" , "https://play.google.com/store/apps/collection/cluster?clp=CiMKIQobdG9wc2VsbGluZ19wYWlkX0FQUExJQ0FUSU9OEAcYAw%3D%3D:S:ANO1ljLDmTo&gsr=CiUKIwohCht0b3BzZWxsaW5nX3BhaWRfQVBQTElDQVRJT04QBxgD:S:ANO1ljKkaLY" , "https://play.google.com/store/apps/collection/cluster?clp=Ch8KHQoXdG9wZ3Jvc3NpbmdfQVBQTElDQVRJT04QBxgD:S:ANO1ljJXOMM&gsr=CiEKHwodChd0b3Bncm9zc2luZ19BUFBMSUNBVElPThAHGAM%3D:S:ANO1ljKY8Zk", "https://play.google.com/store/apps/collection/cluster?clp=ChwKGgoUdG9wc2VsbGluZ19wYWlkX0dBTUUQBxgD:S:ANO1ljI3NIA&gsr=Ch4KHAoaChR0b3BzZWxsaW5nX3BhaWRfR0FNRRAHGAM%3D:S:ANO1ljKgPH8", "https://play.google.com/store/apps/collection/cluster?clp=ChgKFgoQdG9wZ3Jvc3NpbmdfR0FNRRAHGAM%3D:S:ANO1ljKVCGg&gsr=ChoKGAoWChB0b3Bncm9zc2luZ19HQU1FEAcYAw%3D%3D:S:ANO1ljI_yc8"]

for link in links:
	driver.get(link)
	for i in range(0,5):
		lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		time.sleep(2)

	# use hrefs that begin with /store/apps/details
	#app_links = driver.find_elements_by_xpath("//a[substring(@href,string-length(@href) -string-length('/store/apps/details') +1) = '/store/apps/details']")
	app_divs= []
	app_divs = driver.find_elements_by_xpath("//div[@class='b8cIId ReQCgd Q9MA7b']")
	print(len(app_divs))

	id_list = list()
	for app_div in app_divs:
		html_link = app_div.get_attribute('innerHTML')
		app_id = html_link.split('?')[1].split('=')[1].split("\"")[0]
		print(app_id)
		id_list.append(app_id)
	print(id_list)

	writer = open('app_ids', 'a')
	for app_id in id_list:
		writer.write(app_id + '\n')

