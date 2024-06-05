from flask import Flask, request, jsonify
from db import get_db_connection

app = Flask(__name__)

#1 View: Books Details Query
@app.route('/books/details', methods=['GET'])
def get_books_details():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from "GRB"."book_details"')
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(books)

#2 View: Customer Reviews
@app.route('/review', methods=['GET'])
def cs_review():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from "GRB"."cs_review"')
    review = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(review)

#3 View: cs_wishlist
@app.route('/wishlist', methods = ['GET'])
def wishlist ():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from "GRB"."cs_wishlist"')
    wishlist = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(wishlist)

#4. Display Books Customize
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

# 5. DML: INSERT Wishlist Query
# @app.route('/add_author', methods=['POST'])
# def add_author():
#     if request.content_type != 'application/json':
#         return jsonify({'error': 'Content-Type must be application/json'}), 415
    
#     data = request.json
#     required_fields = ["book_id", "title", "author_id", "publisher_id", "category_id", "language_id", "printing_id", "publication_year", "stock", "synopsis", "page"]
    
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'All fields are required'}), 400
    
#     book_id = data['book_id']
#     title = data['title']
#     author_id = data['author_id']
#     publisher_id = data['publisher_id']
#     category_id = data['category_id']
#     language_id = data['language_id']
#     printing_id = data['printing_id']
#     publication_year = data['publication_year']
#     stock = data['stock']
#     synopsis = data['synopsis']
#     page = data['page']
    
#     query = '''
#         INSERT INTO "GRB"."Book"(
#             book_id, title, author_id, publisher_id, category_id, language_id, printing_id, publication_year, stock, synopsis, page
#         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     '''
    
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute(query, (book_id, title, author_id, publisher_id, category_id, language_id, printing_id, publication_year, stock, synopsis, page))
#         conn.commit()
#         response = {'status': 'success'}
#         status_code = 200
#     except Exception as e:
#         conn.rollback()
#         response = {'status': 'error', 'message': str(e)}
#         status_code = 400
#     finally:
#         cursor.close()
#         conn.close()
    
#     return jsonify(response), status_code


#6. DML: INSERT Book Query
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



#7. DML: UPDATE Query

# General Update Function
@app.route('/update', methods=['PUT'])
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

#8. Select General
@app.route('/query', methods=['GET'])
def query_table():
    # Mendapatkan nama tabel dari query string
    table_name = request.args.get('table')
    id = request.args.get('id')

    # Jika nama tabel tidak diberikan, kembalikan pesan kesalahan
    if not table_name:
        return jsonify({'error': 'Nama tabel tidak diberikan'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Eksekusi query SQL
        cursor.execute(f"SELECT * FROM {table_name} order by {id} ")

        # Mengambil semua baris hasil query
        rows = cursor.fetchall()

        # Mengonversi hasil ke dalam format JSON
        # result = [{'id': row[0], 'name': row[1]} for row in rows]  # Misalnya, ubah sesuai dengan struktur tabel Anda

        # Menutup koneksi database
        conn.close()

        # Mengembalikan hasil dalam format JSON
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#10. Customer Delete
@app.route('/customers/delete', methods=['DELETE'])
def delete_customers():
    customer_id = request.args.get('customer_id')
    status = request.args.get('status', 'inactive')  # Default status 'inactive' jika tidak diberikan

    try:
        # Mulai transaksi
        conn = get_db_connection()
        cur = conn.cursor()

        if customer_id:
            # Memeriksa status akun customer tertentu
            cur.execute(f"""
                SELECT ca.status FROM "GRB"."Customer" c
                JOIN "GRB"."Customer_Account" ca ON c.account_id = ca.account_id
                WHERE c.customer_id = {customer_id}
            """)
            
            account_status = cur.fetchone()

            if account_status and account_status[0] == status:
                # Menghapus customer jika statusnya sesuai
                cur.execute(f"""
                    DELETE FROM "GRB"."Customer"
                    WHERE customer_id = {customer_id}
                """)
                conn.commit()
                cur.close()
                return jsonify({"message": "Customer deleted successfully"}), 200
            else:
                conn.rollback()
                cur.close()
                return jsonify({"error": "Customer does not have the specified status or does not exist"}), 400
        else:
            # Menghapus semua customer dengan status tertentu
            cur.execute(f"""
                DELETE FROM "GRB"."Customer" c
                USING "GRB"."Customer_Account" ca
                WHERE c.account_id = ca.account_id AND ca.status = '{status}'
            """)
            deleted_rows = cur.rowcount
            conn.commit()
            cur.close()
            return jsonify({"message": f"{deleted_rows} customers deleted successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    
#10. TCL: Combine Several SQL Statements
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



if __name__ == '__main__':
    app.run(debug=True)
