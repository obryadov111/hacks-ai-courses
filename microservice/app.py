from flask import Flask
from flask import request
from flask_cors import CORS
import alg  
import niquests

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.post("/")
def index():
    if request.method == 'POST':
        input_test = request.json.get('vacancy', '')
        
        if input_test == "":
            try:
                s = niquests.Session(resolver="doh+google://", multiplexed=True)
                input_test = s.get(request.json.get('url', '')).text
            except:
                input_test = ""
        tags = alg.get_tags_vacancy(input_test)
        ans = alg.check(tags)
        return ans
    return "Expected post-method."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)