from flask import Flask, render_template

app = Flask(__name__, template_folder='./frontend/templates')

if __name__ == '__main__':
    app.run(debug=True)