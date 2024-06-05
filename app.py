from flask import Flask, request, jsonify
from db import get_db_connection

app = Flask(__name__)

@app.route('/books/details', methods=['GET'])
def get_books_details():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from "GRB"."book_details"')
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(books)

@app.route('/books', methods=['GET'])
def get_books():
    # Mendapatkan parameter ID buku dari query string
    book_id = request.args.get('id')
    author_id = request.args.get('author_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Memeriksa apakah ID buku diberikan
        if book_id:
            cursor.execute(f'SELECT * FROM "GRB"."Book" WHERE "book_id" = {book_id}')
        elif author_id:
            cursor.execute(f'SELECT * FROM "GRB"."Book" WHERE "author_id" = {author_id}')
        else:
            cursor.execute('SELECT * FROM "GRB"."Book"')

        books = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(books), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 2. DML: INSERT Query
@app.route('/add_book', methods=['POST'])
def add_book():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    data = request.json
    required_fields = ["book_id", "title", "author_id", "publisher_id", "category_id", "language_id", "printing_id", "publication_year", "stock", "synopsis", "page"]
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400
    
    book_id = data['book_id']
    title = data['title']
    author_id = data['author_id']
    publisher_id = data['publisher_id']
    category_id = data['category_id']
    language_id = data['language_id']
    printing_id = data['printing_id']
    publication_year = data['publication_year']
    stock = data['stock']
    synopsis = data['synopsis']
    page = data['page']
    
    query = '''
        INSERT INTO "GRB"."Book"(
            book_id, title, author_id, publisher_id, category_id, language_id, printing_id, publication_year, stock, synopsis, page
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (book_id, title, author_id, publisher_id, category_id, language_id, printing_id, publication_year, stock, synopsis, page))
        conn.commit()
        response = {'status': 'success'}
        status_code = 200
    except Exception as e:
        conn.rollback()
        response = {'status': 'error', 'message': str(e)}
        status_code = 400
    finally:
        cursor.close()
        conn.close()
    
    return jsonify(response), status_code



# 2. DML: UPDATE Query

# General Update Function
@app.route('/update', methods=['POST'])
def update_table():
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    data = request.json
    table = data.get('table')
    values = data.get('values')
    conditions = data.get('conditions')
    
    if not table or not values or not conditions:
        return jsonify({'error': 'Table, values, and conditions are required'}), 400
    
    set_clause = ", ".join([f"{key} = %s" for key in values.keys()])
    condition_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
    
    query = f"UPDATE {table} SET {set_clause} WHERE {condition_clause}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, list(values.values()) + list(conditions.values()))
        conn.commit()
        response = {'status': 'success'}
        status_code = 200
    except Exception as e:
        conn.rollback()
        response = {'status': 'error', 'message': str(e)}
        status_code = 400
    finally:
        cursor.close()
        conn.close()
    
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)

# 3. TCL: Combine Several SQL Statements
@app.route('/execute_transaction', methods=['POST'])
def execute_transaction():
    data = request.json
    queries = data.get('queries')
    
    if not queries:
        return jsonify({'error': 'Queries are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
        response = {'status': 'success'}
        status_code = 200
    except Exception as e:
        conn.rollback()
        response = {'status': 'error', 'message': str(e)}
        status_code = 400
    finally:
        cursor.close()
        conn.close()
    
    return jsonify(response), status_code

@app.route('/query', methods=['GET'])
def query_table():
    # Mendapatkan nama tabel dari query string
    table_name = request.args.get('table')

    # Jika nama tabel tidak diberikan, kembalikan pesan kesalahan
    if not table_name:
        return jsonify({'error': 'Nama tabel tidak diberikan'}), 400

    try:
        # Menghubungkan ke database (misalnya SQLite)
        conn = get_db_connection()
        cursor = conn.cursor()

        # Eksekusi query SQL
        cursor.execute(f"SELECT * FROM {table_name}")

        # Mengambil semua baris hasil query
        rows = cursor.fetchall()

        # Mengonversi hasil ke dalam format JSON
        result = [{'id': row[0], 'name': row[1]} for row in rows]  # Misalnya, ubah sesuai dengan struktur tabel Anda

        # Menutup koneksi database
        conn.close()

        # Mengembalikan hasil dalam format JSON
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 4. select Query
@app.route('/bambang', methods=["POST"])
def select_query():
    data = request.json
    table = data.get('table')

    if not table:
        return jsonify({"error": "Masukkan nama tabel"}), 400
    
    query = f"SELECT * FROM {table}"

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()  # Mengambil hasil query
        response = {"status": "success", "data": results}
        status_code = 200

    except Exception as e:
        response = {"status": "error", "message": str(e)}
        status_code = 400
    
    finally:
        cursor.close()
        conn.close()

    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)
