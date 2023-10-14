
from flask import Flask 

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello this is my branch lelll"

if __name__ == "__main__":
    app.debug = True
    app.run()
