from flask import Flask
from flask import request
import alg  

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    if request.method == 'POST':
        input_test = str(request.json.get('vacancy'))
        tags = alg.get_tags_vacancy(input_test)
        ans = alg.check(tags)
        return ans
    return "Expected post-method."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
