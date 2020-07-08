import flask
from requests import post, get
from flask import request, jsonify
ADDRESS = 'http://localhost:27979'
app = flask.Flask(__name__)
app.config["DEBUG"] = True

access_token = post(f"{ADDRESS}/api/v1/auth", json={'username':'admin','password':'admin'}).json()['access_token']

@app.route('/get', methods=['GET'])

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
    result = get(f"{ADDRESS}/api/v1/tm", headers={"Authorization": f"JWT {access_token}", "Content-Type":"application/json"}, json={"q":q, "slang": slang, "tlang": tlang, "concordance": "true"})
    result_data = result.json()
    return result_data

app.run()