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
	all_possible_class = []
	for x in request.args:
		# get the course name
		course_name = request.args[x]
		try:
			res = session.query(Course).filter(Course.course_name==course_name).all()
			# push the result in array
			# print(res)
			temp = []
			for c in res:
				temp.append({
					"classname":c.classname,
					"weekday":c.weekday,
					"start_time":c.start_time,
					"end_time":c.end_time
				})
			# push all
			all_possible_class.append(temp)

			
			# return make_response({"result":result}, 200)
		except Exception as e:
			print(e)
			return make_response({"result":False}, 400)

	# test print
	# print("------")
	# for x in all_possible_class:
	# 	print(x)

	# print("------")
	
	if len(all_possible_class) == 0:
		return make_response({"result":False}, 200)

	result = np.array(np.meshgrid(*all_possible_class)).T.reshape(-1,len(all_possible_class))
	print(result)

	return make_response({"result":result.tolist()}, 200)

if __name__ == "__main__":
	app.run()