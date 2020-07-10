import flask
from requests import post, get
from flask import request, jsonify
HOST = 'http://localhost:27979'
USERNAME = 'admin'
PASSWORD = 'admin'

app = flask.Flask(__name__)

access_token = post(f"{HOST}/api/v1/auth", json={'username': USERNAME,'password': PASSWORD}).json()['access_token']

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
    result_response = get(f"{HOST}/api/v1/tm", headers={"Authorization": f"JWT {access_token}", "Content-Type":"application/json"}, json={"q":q, "slang": slang, "tlang": tlang})
    result_data = result_response.json()
    matches = []
    if len(result_data['results']):
        results = result_data['results']
        if not results[0]['tu']['source_text'] == " ":
            for result in results:
                match = {
                    'id' : str(results.index(result)),
                    'segment' : result['tu']['source_text'],
                    'translation' : result['tu']['target_text'],
                    'match' : float(result['match']/100)
                }
                matches.append(match)
    return_blob = {'matches': matches}
    return return_blob
    
if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run()