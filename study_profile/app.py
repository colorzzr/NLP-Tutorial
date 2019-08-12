import json

from flask import Flask, escape, request, make_response, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/course')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
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

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

####################################################### Heper ###################################################
import numpy as np



###################################################### FLASK ####################################################

@app.route('/')
@cross_origin()
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/get_tables', methods=['GET'])
@cross_origin()
def get_tables():
	res = session.query(Course).distinct(Course.course_name).with_entities(Course.course_name).all()
	ret_obj = []
	for x in res:
		print(type(x[0]))
		ret_obj.append({
				"key":x[0],
				"value":x[0],
				"text":x[0]
			})
	return make_response({"result":ret_obj}, 200)

@app.route('/get_data', methods=['GET'])
@cross_origin()
def get_data():
	# print(request.args)

	# start looping
	all_possible_class = {
		"fall":[],
		"spring":[]
	}
	for x in request.args:
		# get the course name
		course_name = request.args[x]
		try:
			res = session.query(Course).filter(Course.course_name==course_name).all()
			# push the result in array
			# print(res)
			temp_s = []
			temp_f = []
			for c in res:
				obj = {
					"classname":c.classname,
					"weekday":c.weekday,
					"start_time":c.start_time,
					"end_time":c.end_time,
					"semester": c.semester
				}

				# append depend on semester
				if c.semester == 'F':
					temp_f.append(obj)
				elif c.semester == 'S':
					temp_s.append(obj)
				else:
					temp_f.append(obj)
					temp_s.append(obj)

			# push all depend on semester
			if len(temp_f) != 0:
				all_possible_class["fall"].append(temp_f)
			if len(temp_s) != 0:
				all_possible_class["spring"].append(temp_s)

			
			# return make_response({"result":result}, 200)
		except Exception as e:
			print(e)
			return make_response({"result":False}, 400)


	print(all_possible_class["fall"])
	print(all_possible_class["spring"])

	print("------")

	# permutation all
	result_f = []
	if len(all_possible_class["fall"]):
		result_f = np.array(np.meshgrid(*(all_possible_class["fall"])))\
					.T.reshape(-1,len(all_possible_class["fall"])).tolist()
		print(result_f)

	result_s = []
	if len(all_possible_class["spring"]):
		result_s = np.array(np.meshgrid(*(all_possible_class["spring"])))\
					.T.reshape(-1,len(all_possible_class["spring"])).tolist()
		print(result_s)


	return make_response(
		{
			"result":{
				"fall": result_f,
				"spring": result_s
			}
		}, 200)

if __name__ == "__main__":
	app.run()