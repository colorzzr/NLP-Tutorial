import requests
import json
from bs4 import BeautifulSoup

# cookie
# session = requests.Session()

url = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch?viewId=CourseSearch-FormView&methodToCall=start'
m_page = requests.get(url)
print(m_page.headers['Set-cookie'])



# url = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?deptId=ES%20&divId=ARTSC'
# page = requests.get(url, headers={'Cookie':page.headers['Set-cookie']})
# print(page)s

soup = BeautifulSoup(m_page.text, features="html.parser")

urls = soup.find(id="u214").find_all('input')

for x in urls:
	print("------")
	splited_str = x['value'].replace('\'', '').split(',')
	code, dept = None, None
	if len(splited_str) == 9:
		print(splited_str[4], splited_str[7])
		code, dept = splited_str[4], splited_str[7]
	else:
		print(splited_str[4], splited_str[6])
		code, dept = splited_str[4], splited_str[7]


	url = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?deptId={}%20&divId={}'\
			.format(code, dept)
	page = requests.get(url, headers={'Cookie':m_page.headers['Set-cookie']})
	print(page)
	page = json.loads(page.text)

	aaData = page['aaData']
	print(type(aaData))
	print(len(aaData))