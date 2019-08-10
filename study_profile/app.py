import json

from flask import Flask, escape, request, make_response

app = Flask(__name__)

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/course', echo=True)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class Course(Base):
	__tablename__ = 'Course'
	id = Column(Integer, primary_key=True)
	classname = Column(String)
	weekday = Column(Integer)
	start_time = Column(Integer)
	end_time = Column(Integer)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/get_tables', methods=['GET'])
def get_tables():
	res = session.query(Course).with_entities(Course.classname).all()
	for x in res:
		print(x)
	return "test"

@app.route('/get_data', methods=['GET'])
def get_data():
	classname = json.loads(str(request.get_data().decode('ascii')))

	try:
		res = session.query(Course).filter(Course.classname==classname['classname']).one()
		print(res)
	except Exception as e:
		print(e)

	result = {
			"classname":res.classname,
			"weekday":res.weekday,
			"start_time":res.start_time,
			"end_time":res.end_time
		}
	return make_response({"result":result}, 200)

if __name__ == "__main__":
	app.run()