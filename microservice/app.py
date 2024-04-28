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
        input_text = request.json.get('vacancy', '')
        
        if input_text == "":
            try:
                s = niquests.Session(resolver="doh+google://", multiplexed=True)
                input_text = s.get(request.json.get('url', '')).text
            except:
                input_text = ""
        tags = set()
        if len(input_text) < 30:
            tags = alg.only_one_prof(input_text, alg.all_tags)
            
        tags = tags | alg.get_tags_vacancy(input_text)
        
        ans = alg.check(tags)
        return ans
    return "Expected post-method."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)