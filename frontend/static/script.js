// Espera o DOM carregar completamente
document.addEventListener('DOMContentLoaded', () => {
    fetchBooksAndPopulate();
});

// Função para buscar os livros e popular o DOM
function fetchBooksAndPopulate() {
    fetch('/books_json')
        .then(response => response.json())
        .then(books => {
        const bookList = document.getElementById('book-list');
        books.forEach(book => { // Itera sobre a lista de livros e adiciona ao DOM
            const row = document.createElement('tr');
            row.innerHTML = `
            <td>${book.name}</td>
            <td>${book.author}</td>
            <td>${book.num_copies}</td>
            `;
            bookList.appendChild(row);
            });
        });
}