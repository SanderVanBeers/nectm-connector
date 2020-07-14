from inflection import dasherize
import flask
from requests import post, get
from flask import request, jsonify
from flask.views import MethodView
HOST = 'http://nectm:7979'
USERNAME = 'admin'
PASSWORD = 'admin'

app = flask.Flask(__name__)

#access_token = post(f"{HOST}/api/v1/auth", json={'username': USERNAME,'password': PASSWORD}).json()['access_token']

class MatecatReponse():
    def __init__(self, responseData={'translatedText': 'dit is een test', 'match': 1}, quotaFinished=False, mtLangSupported=None, responseDetails="" , responseStatus= 200, responderId='235', matches = [], exception_code=None):
        self.responseData = responseData
        self.quotaFinished = quotaFinished
        self.mtLangSupported = mtLangSupported
        self.responseDetails = responseDetails
        self.responseStatus = responseStatus
        self.responderId = responderId
        self.matches = matches

    #method to convert the snake_case of instance variables to json standard of kebab-case expected by MateCat (kebab-case raises assign errors in Python)        
    def getDict(self):      
        dictionary = self.__dict__
        return dict([(dasherize(k), v)
                     for (k, v) in dictionary.items()])   

class TmView(MethodView):
    def get(self):
        access_token = post(f"{HOST}/api/v1/auth", json={'username': USERNAME,'password': PASSWORD}).json()['access_token']
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
                        'quality': "75",
                        'reference' : 'dit is een test',
                        'subject' : 'All',
                        'match' : float(result['match']/100),
                        'usage-count' : 0,
                        'created-by' : 'MateCat',
                        'last-updated-by' : 'MateCat',
                        'create-date': 'Tue Jul 07 11:47:11 GMT 2020',
                        'last-update-date' : 'Tue Jul 07 11:47:11 GMT 2020',
                    }
                    matches.append(match)
        return_blob = MatecatReponse(matches = matches)
        return return_blob.getDict()

tm_view = TmView.as_view('tm_api')
app.add_url_rule('/get/', methods=['GET'], view_func=tm_view)
if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run()