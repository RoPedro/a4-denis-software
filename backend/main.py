from flask import Flask, render_template, jsonify, request
from db_queries import Book

# Inicia o app com rotas para o HTML e Javascript.
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Rota principal para renderizar o HTML.
@app.route('/')
def index():
    return render_template('index.html')

# Rota para retornar a lista de livros.
@app.route('/books_json')
def books_json():
    books = Book.list_all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'num_copies': book.num_copies
    } for book in books])

@app.route('/insert_json', methods=['POST'])
def insert_json():
    # Recebe os dados do formulário
    title = request.form['title']
    author = request.form['author']
    num_copies = int(request.form['num_copies'])

    # Cria um novo livro e registra se foi bem sucediddo
    new_book = Book(title=title, author=author, num_copies=num_copies)
    success = new_book.add_book(title, author, num_copies)
   
    # Adereça um resultado dependendo do sucesso da transação 
    if success:
        return jsonify({'status': 'success', 'message': 'Livro adicionado com sucesso!'})
    else:
        return jsonify({'status': 'error', 'message': 'Erro ao adicionar o livro.'})
    


# Habilita o Debug mode
if __name__ == '__main__':
    app.run(debug=True)
