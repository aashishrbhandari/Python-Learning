from flask import Flask, request, send_file, abort

app = Flask(__name__)

FLASK_HOST = '0.0.0.0'
FLASK_PORT = 55050
FLASK_DEBUG = False

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/files/code.me')
def fetch_proxy_pac():
    user_agent = request.headers.get('User-Agent').lower()
    if "firefox" in user_agent:
        try:
            return send_file("some_file.txt")
        except FileNotFoundError:
            abort(404, "No File Specified, But the Flask App Server is Running :-) ")
    else:
        # It is an App other than Default Win App
        try:
            return send_file("some_other_file.txt")
        except FileNotFoundError:
            abort(404, "No File Specified, But the Flask App Server is Running :-) ")


if __name__ == "__main__":
    print(f'[+] Flask App Server Running on {FLASK_HOST}:{FLASK_PORT}')
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)