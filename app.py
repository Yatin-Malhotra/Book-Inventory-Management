from flask import Flask, render_template, request, send_file
import sqlite3
import csv
import io
import os
import re
import json

app = Flask(__name__)

DATABASE = "inventory.db"

def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as con:
            with open("schema.sql", "r") as f:
                con.executescript(f.read())
        print("Database initialized.")
    else:
        print("Database already exists.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_book", methods=["POST"])
def add_book():
    data = request.form
    title = data.get("title")
    author = data.get("author")
    genre = data.get("genre")
    publication_date = data.get("publication_date")
    isbn = data.get("isbn")

    if not title or not author or not genre or not publication_date or not isbn:
        return render_template("index.html", message="All fields are required.", message_type="error")
    
    isbn_cleaned = isbn.replace("-", "")  
    isbn_pattern = r"^978-\d{1,5}-\d{1,7}-\d{1,6}-\d{1}$"

    if len(isbn_cleaned) != 13:
        return render_template(
            "index.html", message="Invalid ISBN format. Must be exactly 13 digits.", message_type="error"
        )

    if not (re.match(isbn_pattern, isbn)):
        return render_template(
            "index.html", message="Invalid ISBN format. Must be exactly 10 or 13 digits.", message_type="error"
        )


    try:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Inventory (title, author, genre, publication_date, isbn) VALUES (?, ?, ?, ?, ?)",
                (title, author, genre, publication_date, isbn),
            )
            con.commit()
        return render_template("index.html", message="Book added successfully!", message_type="success")
    except sqlite3.IntegrityError:
        return render_template("index.html", message="ISBN already exists. Please provide a unique ISBN.", message_type="error")

@app.route("/filter_books", methods=["GET"])
def filter_books():
    title = request.args.get("title", "")
    author = request.args.get("author", "")
    genre = request.args.get("genre", "")

    query = """
    SELECT * FROM Inventory 
    WHERE title LIKE ? AND author LIKE ? AND genre LIKE ?
    """
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(query, (f"%{title}%", f"%{author}%", f"%{genre}%"))
        results = cur.fetchall()

    return render_template("index.html", books=results)

@app.route("/export", methods=["GET"])
def export_data():
    format = request.args.get("format", "json")
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Inventory")
        rows = cur.fetchall()

    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Entry ID", "Title", "Author", "Genre", "Publication Date", "ISBN"])
        writer.writerows(rows)
        output.seek(0)

        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype="text/csv",
            as_attachment=True,
            download_name="books.csv",
        )
    else:
        books_data = []
        for row in rows:
            book_data = {
                "Entry ID": row[0],
                "Title": row[1],
                "Author": row[2],
                "Genre": row[3],
                "Publication Date": row[4],
                "ISBN": row[5],
            }
            books_data.append(book_data)

        json_filename = "books_inventory.json"
        output = io.BytesIO(json.dumps(books_data, indent=4).encode('utf-8'))

        return send_file(
            output,
            mimetype="application/json",
            as_attachment=True,
            download_name=json_filename,
        )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
