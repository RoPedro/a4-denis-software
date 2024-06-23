from flask import Flask, render_template, jsonify
from db_queries import Book

# Inicia o app com rotas para o HTML e Javascript.
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Rota para retornar a lista de livros.
@app.route('/books_json')
def books_json():
    books = Book.list_all()
    return jsonify([{
                     'name': book.title,
                     'author': book.author,
                     'num_copies': book.num_copies}
                     for book in books])

# Rota principal para renderizar o HTML.
@app.route('/')
def index():
    return render_template('index.html')

# Habilita o Debug mode
if __name__ == '__main__':
    app.run(debug=True)