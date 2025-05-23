import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

from data_models import db, Author, Book

DATE_FORMAT = "%Y-%m-%d"

load_dotenv()

app = Flask(__name__)

# Absolute path to SQLite database
db_path = os.path.join(os.getcwd(), "data", "library.sqlite")
os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Create 'data' folder if not exists

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

# Connects Flask app to Flask-SQLAlchemy
db.init_app(app)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Handles adding a new author to the database.

    Supports both GET and POST requests:
    - **GET request**: Renders the author addition form.
    - **POST request**: Processes form data to create a new author.
      - Validates birthdate and optional date of death.
      - Adds the author to the database if valid.
      - Redirects back with a flash message in case of errors.

    Returns:
        Response: A rendered template for GET requests or a redirect for POST requests.
    """
    if request.method == "GET":
        return render_template("add_author.html")
    elif request.method == "POST":
        # collect author's data from form request
        author_name = request.form["name"]

        try:
            author_birth_date = datetime.strptime(request.form["birthdate"], DATE_FORMAT)
        except ValueError as e:
            flash("Incorrect birth date! Author not added.")
            return redirect(url_for("add_author"))

        date_of_death = request.form["date_of_death"]
        author_date_of_death = None
        if date_of_death != "":
            try:
                author_date_of_death = datetime.strptime(request.form["date_of_death"], DATE_FORMAT)
            except ValueError as e:
                flash("Incorrect date of death! Author not added.")
                return redirect(url_for("add_author"))

        # add new author to the db
        new_author = Author(
            name=author_name,
            birth_date=author_birth_date,
            date_of_death=author_date_of_death
        )
        db.session.add(new_author)
        db.session.commit()

        flash("New author has been saved to db.")

        return redirect(url_for("add_author"))


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Handles adding a new book to the database.

    Supports both GET and POST requests:
    - **GET request**: Renders the book addition form with a list of available authors.
    - **POST request**: Processes form data to create a new book.
        - Retrieves book details from the form (ISBN, title, publication year, author).
        - Adds the book to the database if valid.
        - Redirects back with a success message.

    Returns:
        Response: A rendered template for GET requests or a redirect for POST requests.
    """
    if request.method == "GET":
        return render_template("add_book.html", authors=Author.query.all())
    elif request.method == "POST":
        book_isbn = request.form["isbn"]
        book_title = request.form["title"]
        book_publication_year = request.form["publication_year"]
        book_author_id = request.form["author"]

        new_book = Book(
            isbn=book_isbn,
            title=book_title,
            publication_year=book_publication_year,
            author_id=book_author_id
        )

        db.session.add(new_book)
        db.session.commit()

        flash("New book has been saved to db.")

        return redirect(url_for("add_book"))


@app.route("/")
def home():
    """Renders the homepage with a list of books, supporting sorting and searching.

    Retrieves books from the database and applies optional sorting and search filters:
    - **Sorting**: Supports sorting by title or author in ascending or descending order.
    - **Searching**: Filters books based on a case-insensitive search query for titles.

    Query Parameters:
        sort (str, optional): Sorting order, either "asc" or "desc".
        sort_by (str, optional): Field to sort by, either "title" or "author".
        search (str, optional): Search query to filter books by title.

    Returns:
        Response: A rendered HTML template displaying the filtered and sorted book list.
    """
    sort_order = request.args.get("sort")
    sort_by = request.args.get("sort_by")
    search_query = request.args.get("search", "").strip()

    books_query = db.session.query(Book)

    # Apply sorting
    if sort_order in ["asc", "desc"] and sort_by in ["title", "author"]:
        if sort_by == "title":
            books_query = books_query.order_by(Book.title.asc() if sort_order == 'asc' else Book.title.desc())
        elif sort_by == "author":
            books_query = books_query.join(Author).order_by(
                Author.name.asc() if sort_order == 'asc' else Author.name.desc())

    # Apply search filter
    if search_query:
        books_query = books_query.filter(Book.title.ilike(f"%{search_query}%"))

    books = books_query.all()
    return render_template("home.html",
        books=books,
        search_query=search_query,
        sort_order=sort_order,
        sort_by=sort_by
    )


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete(book_id):
    """Deletes a book from the database and removes its author if they have no other books.

    This route handles the deletion of a book by its ID. If the book's author has no other books
    remaining after deletion, the author is also removed from the database.

    Args:
        book_id (int): The ID of the book to be deleted.

    Returns:
        Response: Redirects to the home page after deletion.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    remaining_books = Book.query.filter_by(author_id=author.id).count()

    if remaining_books == 0:
        db.session.delete(author)
        db.session.commit()

    flash("Book was successfully deleted.")
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
