# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from google.cloud import datastore
from flask import Flask, request, render_template
from dotenv import load_dotenv
from os import getenv, environ



# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    GOOGLE_MAP_API_KEY = getenv('GOOGLE_MAP_API_KEY') or environ('GOOGLE_MAP_API_KEY')
    return render_template('main.html', key=GOOGLE_MAP_API_KEY)

@app.route('/api/add_entity',methods=["POST"])
def api_add_entity():
    add_entity(
        request.form["first_name"],
        request.form["last_name"],
        request.form["latitude"],
        request.form["longitude"],
        request.form["stuff"],
        request.form["amount"],
        request.form["have"]
        )
    return "Add Entity"

@app.route('/api/query_entity')
def api_query_entity():
    return query_entity()


def add_entity(first_name = "",last_name = "",latitude = 0.0,longitude = 0.0,stuff = "",amount = 0, have = True):
    datastore_client = datastore.Client()
    task_key = datastore_client.key("user")
    task = datastore.Entity(key=task_key)
    task.update({
        "first_name": first_name,
        "last_name": last_name,
        "latitude": latitude,
        "longitude": longitude,
        "stuff": stuff,
        "amount": amount,
        "have": have,
        "done": False
    })
    datastore_client.put(task)
    # print('Saved {}'.format(task.key.id))


def query_entity():
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="user")
    # query.add_filter("done", ""="", False)
    results = list(query.fetch())
    for i in range(len(results)):
        results[i]["id"]=results[i].id
    res = {"result": results}
    return res



#  def delete_entity(kind,name):
#      key = datastore_client.key(kind, name)
#      datastore_client.delete(key)




if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
