import requests
import json
from bs4 import BeautifulSoup

url = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?deptId=ES%20&divId=ARTSC'
page = requests.get(url, headers={'Cookie':'kualiSessionId=95af0277-abcf-42d4-9f39-ca31e807def5; JSESSIONID=CF4A57CE3520445A98C6EA67A05FC57C.w1; _ga=GA1.2.461670942.1560481774; _gcl_au=1.1.1342980630.1560481876; _fbp=fb.1.1560481876526.1828524231; __utma=264236318.461670942.1560481774.1565314255.1565314255.1; __utmc=264236318; __utmz=264236318.1565314255.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __atuvc=2%7C32; __atuvs=5d4ccdafde920e5a001; __utmb=264236318.9.10.1565314255'})
page = json.loads(page.text)

aaData = page['aaData']
print(type(aaData))
print(len(aaData))

for course in aaData:
	print("------")
	# for detail in course:
	# 	print(detail)

	print(course[1])
	soup = BeautifulSoup(course[1], features="html.parser")
	print(soup.a['href'].split('/')[2])
	

print("\n------Detail------\n")
course = 'ESS262H1F20199'
url='http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=%s'%course
# print(url)
page = requests.get(url).text
# print(page)
soup = BeautifulSoup(page, features="html.parser")

tr = soup.table.find_all(role="presentation")

header=['Activiy', 'Day and Time', 'Instructor', 'Location', 'Class Size', 'Current Enroll', 'Waitlist', 'Delivery Mode']
count = 0
for x in tr:
	print("------")
	print(header[count])
	if x.span != None:
		print(x.span.text.replace('\n', ''))

	count = (count+1)%7

