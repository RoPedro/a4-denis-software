// Espera o DOM carregar completamente
document.addEventListener('DOMContentLoaded', () => {
    fetchBooksAndPopulate();
    
    // ---------------------------------------------------------

    const addBookBtn = document.getElementById('add-book-btn');
    const addBookModal = document.getElementById('addBookModal');

    addBookBtn.addEventListener('click', adicionarLivro);

    /*
    removerLivro.addEventListener('click', removerLivro);
    atualizarLivro.addEventListener('click', atualizarLivro);
    const addBookModal = document.getElementById('addBookModal');
    const addBookBtn = document.getElementById('add-book-btn');
    */
});

// Função para buscar os livros e popular o DOM
function fetchBooksAndPopulate() {
    fetch('/books_json')
        .then(response => {
            console.log('Response status:', response.status);
            return response.json()
        })
        .then(books => {
            console.log(books);
            const bookList = document.getElementById('book_tbody');

            bookList.innerHTML = '';

            books.forEach(book => { // Itera sobre a lista de livros e adiciona ao DOM
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${book.id}</td>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.num_copies}</td>
                `;
                bookList.appendChild(row);
            });
        });
}

// Função para adicionar um novo livro
function adicionarLivro() {
    const titleInput = document.getElementById('titulo');
    const authorInput = document.getElementById('autor-modal');
    const numCopiesInput = document.getElementById('copias');
    const addBookModal = document.getElementById('addBookModal');

    // Create FormData object with input values
    const formData = new FormData();
    formData.append('title', titleInput.value);
    formData.append('author', authorInput.value);
    formData.append('num_copies', numCopiesInput.value);

    // Send POST request to the server
    fetch('/insert_json', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || 'Erro ao adicionar livro');
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        // Hide the modal
        bootstrap.Modal.getInstance(addBookModal).hide();
        // Clear input fields
        titleInput.value = '';
        authorInput.value = '';
        numCopiesInput.value = '';
    })
    .catch(error => {
        console.error('ERROR:', error);
        alert('Erro ao adicionar livro');
    });
}

// Exclui um livro de forma assíncrona
async function deleteBook() {
    // ID Dummy (Modificar para pegar o valor no HTML)
    const dummyId = 13;

    try {
        const response = await fetch('/delete_json', { // Envia o ID para o servidor
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ book_id: dummyId })
        });

        if (!response.ok) {
            throw new Error(await response.text() || 'Erro ao excluir livro');
        }

        const data = await response.json();
        alert(data.message);
    
        // Muda a mensagem de erro de acordo com o tipo de erro
    } catch (error) {
        if (error.message.includes('Livro não encontrado')) {
            alert('Livro não encontrado');
        } else if(error.message.includes('ID do livro inválido')){
            alert('ID do livro inválido');
        }else {
            console.error('ERROR:', error);
            alert('Erro ao excluir livro');
        }
    }
}
function fetchBooksAndPopulate() {
    fetch('/books_json')
        .then(response => {
            console.log('Response status:', response.status);
            return response.json()
        })
        .then(books => {
            console.log(books);
            const bookList = document.getElementById('book_tbody');

            bookList.innerHTML = '';

            books.forEach(book => { // Itera sobre a lista de livros e adiciona ao DOM
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${book.id}</td>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.num_copies}</td>
                    <td><i class="fas fa-trash-alt text-danger" style="cursor: pointer;" onclick="confirmDelete(${book.id}, '${book.title}')"></i></td>
                `;
                bookList.appendChild(row);
            });
        });
}

function confirmDelete(bookId, bookTitle) {
    if (confirm(`Confirma exclusão do livro ${bookTitle}?`)) {
        deleteBook(bookId);
    }
}

async function deleteBook(bookId) {
    try {
        const response = await fetch('/delete_json', { // Envia o ID para o servidor
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ book_id: bookId })
        });

        if (!response.ok) {
            throw new Error(await response.text() || 'Erro ao excluir livro');
        }

        const data = await response.json();
        alert(data.message);
    
        // Muda a mensagem de erro de acordo com o tipo de erro
    } catch (error) {
        if (error.message.includes('Livro não encontrado')) {
            alert('Livro não encontrado');
        } else if(error.message.includes('ID do livro inválido')){
            alert('ID do livro inválido');
        }else {
            console.error('ERROR:', error);
            alert('Erro ao excluir livro');
        }
    }
}
function fetchBooksAndPopulate() {
    fetch('/books_json')
       .then(response => {
            console.log('Response status:', response.status);
            return response.json()
        })
       .then(books => {
            console.log(books);
            const bookList = document.getElementById('book_tbody');

            bookList.innerHTML = '';

            books.forEach(book => { // Itera sobre a lista de livros e adiciona ao DOM
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${book.id}</td>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.num_copies}</td>
                    <td>
                        <i class="fas fa-trash-alt text-danger" style="cursor: pointer;" onclick="confirmDelete(${book.id}, '${book.title}')"></i>
                        <i class="fas fa-pen text-primary" style="cursor: pointer;" onclick="confirmEdit(${book.id}, '${book.title}', '${book.author}', ${book.num_copies})"></i>
                    </td>
                `;
                bookList.appendChild(row);
            });
        });
}

function confirmEdit(bookId, bookTitle, bookAuthor, bookNumCopies) {
    if (confirm(`Confirma edição do livro ${bookTitle}?`)) {
        editBook(bookId, bookTitle, bookAuthor, bookNumCopies);
    }
}

function editBook(bookId, bookTitle, bookAuthor, bookNumCopies) {
    const titleInput = prompt(`Novo título para o livro ${bookTitle}:`, bookTitle);
    const authorInput = prompt(`Novo autor para o livro ${bookTitle}:`, bookAuthor);
    const numCopiesInput = prompt(`Novo número de cópias para o livro ${bookTitle}:`, bookNumCopies);

    if (titleInput!== null && authorInput!== null && numCopiesInput!== null) {
        const updatedBook = {
            id: bookId,
            title: titleInput,
            author: authorInput,
            num_copies: parseInt(numCopiesInput, 10)
        };

        // Envia requisição para atualizar o livro no servidor
        fetch('/update_book', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedBook)
        })
       .then(response => response.json())
       .then(data => {
            console.log(`Livro ${bookTitle} atualizado com sucesso!`);

            // Atualiza a lista de livros
            fetchBooksAndPopulate();

            // Registra as alterações no site
            const logElement = document.getElementById('log');
            const logText = `Livro ${bookTitle} editado: título = ${titleInput}, autor = ${authorInput}, número de cópias = ${numCopiesInput}`;
            logElement.innerHTML += `<p>${logText}</p>`;
        })
       .catch(error => console.error('Erro ao atualizar livro:', error));
    }
}
