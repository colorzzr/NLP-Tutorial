import requests
import json
from bs4 import BeautifulSoup

# Postgres
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/course', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class Course(Base):
	__tablename__ = 'Course'
	id = Column(Integer, primary_key=True)
	classname = Column(String)
	weekday = Column(Integer)
	start_time = Column(Integer)
	end_time = Column(Integer)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


url = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?deptId=ES%20&divId=ARTSC'
page = requests.get(url, headers={'Cookie':'kualiSessionId=62484105-2b10-4161-80dc-1360c1780f03; JSESSIONID=77F353585DDFCF04F7C24CA5623DEE2B.w2; _ga=GA1.2.461670942.1560481774; _gcl_au=1.1.1342980630.1560481876; _fbp=fb.1.1560481876526.1828524231; __utmz=264236318.1565314255.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __atuvc=12%7C32; __utma=264236318.461670942.1560481774.1565322436.1565403409.3; __utmc=264236318; __utmt=1; __utmb=264236318.1.10.1565403409'})
page = json.loads(page.text)

aaData = page['aaData']
print(type(aaData))
print(len(aaData))


def add_course_2_db(course):
	# course = 'ESS262H1F20199'
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
		# print("------")
		# print(header[count])
		# if x.span != None:
		# 	print(x.span.text.replace('\n', ''))

		# get info
		if count == 0:
			lec = "%s %s"%(course, str(x.span.text.replace('\n', '').replace('\r', '')))
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
					weekday = 0
				elif (lec_detail[0]) == '\rTUESDAY':
					weekday = 1
				elif (lec_detail[0]) == '\rWEDNESDAY':
					weekday = 2
				elif (lec_detail[0]) == '\rTHURSDAY':
					weekday = 3
				elif (lec_detail[0]) == '\rFRIDAY':
					weekday = 4

				# split time
				time = lec_detail[1].replace(':', '-').split('-')
				start_time = int(time[0])
				end_time = int(time[2])

				session.add(Course(classname=lec, weekday=weekday, start_time=start_time, end_time=end_time))
				session.commit()
				# print(int(time[0]), int(time[2])) 

		count = (count+1)%8


for course in aaData:
	print("------")
	# for detail in course:
	# 	print(detail)

	print(course[1])
	soup = BeautifulSoup(course[1], features="html.parser")
	print(soup.a['href'].split('/')[2])
	course = soup.a['href'].split('/')[2]
	add_course_2_db(course)
