import requests
import json
from bs4 import BeautifulSoup

# Postgres
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/course')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class Course(Base):
	__tablename__ = 'Course'
	id = Column(Integer, primary_key=True)
	course_name = Column(String)
	classname = Column(String)
	weekday = Column(Integer)
	start_time = Column(Integer)
	end_time = Column(Integer)
	semester = Column(String)

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


# url = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?deptId=ES%20&divId=ARTSC'
# page = requests.get(url, headers={'Cookie':'kualiSessionId=b5a34b27-6add-46ae-94d6-5bd2a81708ce; JSESSIONID=5313617B3ACD4ACBAB9E48FE1669D22C.w1; _ga=GA1.2.461670942.1560481774; _gcl_au=1.1.1342980630.1560481876; _fbp=fb.1.1560481876526.1828524231; __utmz=264236318.1565314255.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __atuvc=14%7C32; __utmc=264236318; __utma=264236318.461670942.1560481774.1565573473.1565576633.10; __utmt=1; __utmb=264236318.5.10.1565576633'})
# print(page)
# page = json.loads(page.text)

# aaData = page['aaData']
# print(type(aaData))
# print(len(aaData))


def add_course_2_db(course):
	# course = 'ESS262H1F20199'
	# ESS262 is course code
	# H1 IDK
	# F/S/Y is Fall or Spring
	print(course[:6])
	print(course[8])
	url='http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=%s'%course
	# print(url)
	page = requests.get(url).text
	# print(page)
	soup = BeautifulSoup(page, features="html.parser")

	# if there is no table
	if soup.table == None:
		return
	tr = soup.table.find_all(role="presentation")
	

	header=['Activiy', 'Day and Time', 'Instructor', 'Location', 'Class Size', 'Current Enroll', 'Waitlist', 'Delivery Mode']
	count = 0
	for x in tr:

		# get info
		if count == 0:
			lec = "%s %s"%(course[:6], str(x.span.text.replace('\n', '').replace('\r', '')))
		elif count == 1:
			lec_time = x.span.text.replace('\n', '')
			lec_time_arr = lec_time.split('\n')
			# split the time slots
			for y in lec_time_arr:
				lec_detail = str(y).split(' ')
				if lec_detail == ['']:
					continue

				print(lec_detail)

				weekday = 0
				# get the weekday
				if (lec_detail[0]) == '\rMONDAY':
					weekday = 1
				elif (lec_detail[0]) == '\rTUESDAY':
					weekday = 2
				elif (lec_detail[0]) == '\rWEDNESDAY':
					weekday = 3
				elif (lec_detail[0]) == '\rTHURSDAY':
					weekday = 4
				elif (lec_detail[0]) == '\rFRIDAY':
					weekday = 5

				# split time
				time = lec_detail[1].replace(':', '-').split('-')
				start_time = int(time[0])
				end_time = int(time[2])

				session.add(Course(
								course_name=course[:6], 
								classname=lec, 
								weekday=weekday, 
								start_time=start_time, 
								end_time=end_time,
								semester=course[8]
							))
				session.commit()
				# print(int(time[0]), int(time[2])) 

		count = (count+1)%8



def loop_over_all_data(aaData):
	for course in aaData:
		print("------")

		print(course[1])
		soup = BeautifulSoup(course[1], features="html.parser")
		print(soup.a['href'].split('/')[2])
		course = soup.a['href'].split('/')[2]
		add_course_2_db(course)


# request to get cookie
url = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch?viewId=CourseSearch-FormView&methodToCall=start'
m_page = requests.get(url)
print(m_page.headers['Set-cookie'])



soup_temp = BeautifulSoup(m_page.text, features="html.parser")
urls = soup_temp.find(id="u214").find_all('input')

for x in urls:
	print("------")
	splited_str = x['value'].replace('\'', '').split(',')
	code, dept = None, None
	if len(splited_str) == 9:
		print(splited_str[4], splited_str[7])
		code, dept = splited_str[4], splited_str[7]
	else:
		print(splited_str[4], splited_str[6])
		code, dept = splited_str[4], splited_str[6]

	# print(code, dept)
	url = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?deptId={}%20&divId={}'\
			.format(code, dept)
	page = requests.get(url, headers={'Cookie':m_page.headers['Set-cookie']})
	print(page)
	page = json.loads(page.text)

	aaData = page['aaData']
	print(type(aaData))
	print(len(aaData))
	loop_over_all_data(aaData)