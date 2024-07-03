from flask import Flask, render_template, jsonify, request 
from db_queries import Book
from db_connect import engine
from db_daos import BookDAO

connection = engine.connect()
book_dao = BookDAO(connection)

# Inicia o app com rotas para o HTML e Javascript.
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Rota principal para renderizar o HTML.
@app.route('/')
def index():
    return render_template('index.html')

# Rota para retornar a lista de livros.
@app.route('/books_json')
def books_json():
    books = book_dao.list_all() 
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'num_copies': book.num_copies
    } for book in books])

# Rota para inserção de livros.
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

# Roda para exclusão de livros
@app.route('/delete_json', methods=['DELETE'])
def delete_book_by_id():
    data = request.get_json()
    if data is None:
        return jsonify({'status': 'error', 'message': 'JSON não encontrado'}), 400
    book_id = data.get('book_id')

    # Checa se o ID do livro é valido
    if not isinstance(book_id, int): 
        try:
            book_id = int(book_id)
        except ValueError:
            return jsonify({'status': 'error', 'message': 'ID do livro invalido'}), 400

    # Retorna diferentes respostas dependendo do sucesso da transação
    success = Book.delete_book(book_id)
    if success:
        return jsonify({'status': 'success', 'message': 'Livro excluído com sucesso'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Livro não encontrado'}), 404

@app.route('/update_details_json' , methods=['PUT'])
def update_book_details_by_id():
    data = request.get_json()
    if data is None:
        return jsonify({'status': 'error', 'message': 'JSON não encontrado'}), 400
    book_id = data.get('book_id')
    new_title = data.get('title')
    new_author = data.get('author')

    # Checa se o ID do livro é valido
    if not isinstance(book_id, int): 
        try:
            book_id = int(book_id)
        except ValueError:
            return jsonify({'status': 'error', 'message': 'ID do livro invalido'}), 400

    # Retorna diferentes respostas dependendo do sucesso da transação
    success = Book.update_title_author(book_id, new_title, new_author)
    if success:
        return jsonify({'status': 'success', 'message': 'Livro atualizado com sucesso'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Livro não encontrado'}), 404

# Habilita o Debug mode
if __name__ == '__main__':
    app.run(debug=True)
