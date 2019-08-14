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

res = session.query(Course).distinct(Course.course_name).all()
print(len(res))

# es
from elasticsearch import Elasticsearch
es = Elasticsearch()
# course name
index_name = "course"
# create new index
es.indices.delete(index=index_name, ignore=[400, 404])
es.indices.create(index = index_name, body = {
    "mappings": {
        "properties" : {
            "text" : {
                "type" : "completion"
            },
            "title" : {
                "type": "keyword"
            }
        }
    }
})

for x in res:
	body = {
		"key":x.course_name,
		"value":x.course_name,
		"text":x.course_name
	}

	es.index(index=index_name, doc_type='_doc', body=body)

