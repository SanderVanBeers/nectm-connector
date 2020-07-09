from flask import Flask
from requests import post, get
from flask_restful import Resource, Api
from flask import request, jsonify
HOST = 'http://localhost:27979'
USERNAME = 'admin'
PASSWORD = 'admin'

app = flask.Flask(__name__)
app.config["DEBUG"] = True

access_token = post(f"{HOST}/api/v1/auth", json={'username': USERNAME,'password': PASSWORD}).json()['access_token']

@app.route('/get', methods=['GET'])

class match(self):
    def __init__:
        self.id =
        self.segment =          #result['tu']['source_text']
        self.translation =      #result['tu']['target_text']
        self.quality =          #?
        self.reference =        #result_data['query']
        self.subject =          #~tag?
        self.match =            #result['match']
        self.usage-count =
        self.created-by = 
        self.last-updated-by = 
        self.create-date =
        self.last-update-date = 
    def get(self):
        pass

def get_fuzzy_match():
    data = request.get_json()
    q = data['q']
    langpair = data['langpair']
    if '|' in langpair:
        slang = langpair.split('|')[0].split('-')[0]
        tlang = langpair.split('|')[1].split('-')[0]
    else:
        slang = langpair.split('-')[0]
        tlang = langpair.split('-')[1]
    result = get(f"{HOST}/api/v1/tm", headers={"Authorization": f"JWT {access_token}", "Content-Type":"application/json"}, json={"q":q, "slang": slang, "tlang": tlang, "concordance": "true"})
    result_data = result.json()
    return result_data

app.run()