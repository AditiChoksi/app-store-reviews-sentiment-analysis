import re
import time
import sys
start = time.time()

regex = re.compile('[^a-zA-Z]')

def process_text(text):
	#print('Emoji version: ' + text)
	
	text = text.encode('ascii', 'ignore').decode('ascii')
	#print('Demoji version: ' + text)
	text = regex.sub(' ', text)
	text = text.lower();
	#remove tags
	#text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
	# remove special characters and digits
	#text=re.sub("(\\d|\\W)+"," ",text)

	#print(text)
	return text

#for curr in range(1,7):
curr = sys.argv[1]
reader = open('./review_dump/'+str(curr), 'r')
writer = open('./review_filtered/'+ str(curr)  +'.csv', 'a')
print('Running')
header_complete = False
counter = 0
months = set(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August' , 'September' , 'October', 'November', 'December'])
for line in reader:
	if line.strip() == 'Similar':
		print('Terminating...')
		break
	if line.strip() == "":
		break
	line = line.strip()
	if(header_complete == False):
		if line == 'User reviews':
			header_complete = True
		else:
			counter = counter+1
			#print('Skipping: ' + line)
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
			#print("Count: " + count_line)
			filtered = process_text(review_line)
			#print(filtered)
			to_write = date_line + "," + count_line + "," + filtered + '\n' 
		else:
			#print(count_line + "!= numeric")
			#print("Count: 0")
			filtered = process_text(count_line)
			#print(filtered)
			to_write = date_line + "," + "0" + "," + filtered + '\n' 
		
		writer.write(to_write)
		
print("Done with " + str(curr))

