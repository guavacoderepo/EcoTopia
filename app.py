from flask import Flask
from src import create_app

app = create_app()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    
    app.run(debug=True)