from flask import Flask, request
from infer import img_arr_from_base64, get_openpose

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return "Welcome to openpose service"


@app.route('/openpose', methods=[ 'POST'])
def openpose():
    bytes = request.get_data()
    # print("bytes:", bytes)
    rgb_arr = img_arr_from_base64(bytes)

    jresults = get_openpose(rgb_arr)
    return jresults

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)