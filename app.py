from flask import Flask, render_template
from flask.ext.script import Manager, Server
from pymongo import MongoClient
import json
import tweets_by_keywords as tbk 
import tweets_user as tu 
import facebook as fb
from celery import Celery


app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

def make_celery(app):
    celery = Celery('app', broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)

@celery.task()
def tbk_worker(keyword):
	tbk.main(keyword)

@celery.task()
def fb_worker(keyword):
	fb.fb_data(keyword)

client = MongoClient('localhost', 27017)
db = client['project-1']

user_collection = db['User']

@app.route("/")
def main():
	tbk_worker.delay('yo')
	tbk_worker.delay('abc')
	# user_collection.insert_one(a)
	return render_template('index.html') 

if __name__ == "__main__":
    app.run(debug=True)