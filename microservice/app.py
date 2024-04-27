from flask import Flask
from flask import request
from flask_cors import CORS
import alg  

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.post("/")
def index():
    if request.method == 'POST':
        input_test = str(request.json.get('vacancy'))
        
        if input_test == "":
            try:
                url = str(request.json.get('url'))
                response = requests.get(url)
                print(response.content)
                soup = BeautifulSoup(response.content, 'lxml')
                input_test = soup.getText()
            except:
                input_test = ""
        tags = alg.get_tags_vacancy(input_test)
        ans = alg.check(tags)
        return ans
    return "Expected post-method."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)