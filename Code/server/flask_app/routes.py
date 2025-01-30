from flask_app import app, db, bcrypt, jwt, cache
from flask import url_for, request, jsonify, send_file
from flask_app.models import User, Section, Book, BookRequest, Feedback, user_books, completed_books
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request, get_current_user
from flask_app.tasks import daily_remainder, monthly_activity_report, generate_csv_file
from datetime import datetime, timedelta
from sqlalchemy import insert, delete
import os
import matplotlib.pyplot as plt
import seaborn as sns
import secrets
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity['role'] != 'librarian':
            return jsonify({"message": "Librarian access required"}), 403
        return fn(*args, **kwargs)
    return decorator

@app.route('/', methods=['GET'])
def get_data():
    user_id = request.args.get('user_id') or None
    if user_id:
        user = User.query.get(user_id)
    sections = Section.query.all()
    data = []
    for section in sections:
        books = Book.query.filter_by(section_id=section.id).all()
        books_data = []
        for book in books:
            feedbacks = Feedback.query.filter_by(book_id=book.id).all()
            avg_rating = sum([feedback.rating for feedback in feedbacks]) / len(feedbacks) if feedbacks else 0
            status = BookRequest.query.filter_by(book_id=book.id, user_id=user_id).first() or None
            completed = db.session.query(completed_books).filter_by(book_id=book.id, user_id=user_id).first() or None
            books_data.append({
                "id": book.id, 
                "name": book.name, 
                "authors": book.authors,
                "status": status.request_status if status else None,
                "avg_rating": avg_rating,
                "reviews": [{'user': feedback.user.username, 'rating': feedback.rating, 'review': feedback.review} for feedback in feedbacks],
                "completed": bool(completed)
                })
                
        data.append({
            "id": section.id,
            "name": section.name,
            "description": section.description,
            "books": books_data
        })
    return jsonify(data)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    search_category = data['search_category']
    search_query = data['search_query']
    books, sections = [], []
    
    if search_category == 'book':
        books = Book.query.filter(Book.name.like(f'%{search_query}%')).all()
    elif search_category == 'section':
        sections = Section.query.filter(Section.name.like(f'%{search_query}%')).all()
    elif search_category == 'author':
        books = Book.query.filter(Book.authors.like(f'%{search_query}%')).all()
    
    return jsonify({
        'books': [{'id': book.id, 'name': book.name, 'authors': book.authors, 'section': {'name': book.section.name}} for book in books],
        'sections': [{'id': section.id, 'name': section.name, 'books': [{'id': book.id, 'name': book.name, 'authors': book.authors} for book in section.books]} for section in sections]
    })

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
        return jsonify({"access_token": access_token, "role": user.role, "id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/sections', methods=['GET'])
@jwt_required()
@admin_required
def sections():
    sections = Section.query.all()
    sections_data = [{'id': section.id, 'name': section.name, 'description': section.description, 'books': [{'id': book.id, 'name': book.name, 'authors': book.authors, 'section_id':section.id} for book in section.books]} for section in sections]
    return jsonify(sections_data)

@app.route('/add-section', methods=['POST'])
@jwt_required()
@admin_required
def add_section():
    data = request.get_json()
    new_section = Section(name=data['name'], description=data['description'])
    db.session.add(new_section)
    db.session.commit()
    return jsonify({"message": "Section added successfully"}), 201
    
@app.route('/update-section/<int:section_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_section(section_id):
    data = request.get_json()
    section = Section.query.get_or_404(section_id)
    section.name = data['name']
    section.description = data['description']
    db.session.commit()
    return jsonify({"message": "Section updated successfully"}), 200

@app.route('/delete-section/<int:section_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)
    section_books = Book.query.filter_by(section_id=section_id).all()
    for book in section_books:
        db.session.query(completed_books).filter_by(book_id=book.id).delete()
        db.session.query(Feedback).filter_by(book_id=book.id).delete()
        db.session.delete(book)
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "Section deleted successfully"}), 200

@app.route('/books', methods=['GET'])
@jwt_required()
@admin_required
def books():
    existing_books = Book.query.all()
    books_data = [{'id': book.id, 'name': book.name, 'authors': book.authors, 'pdf': book.pdf, 'section': book.section.name} for book in existing_books]
    return jsonify(books_data)

    
def save_pdf(form_pdf):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_pdf.filename)
    pdf_filename = random_hex + f_ext
    pdf_directory = os.path.join(app.root_path, 'static', 'books')

    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    pdf_path = os.path.join(pdf_directory, pdf_filename)

    form_pdf.save(pdf_path)

    return pdf_filename

def delete_pdf(pdf_filename):
    pdf_directory = os.path.join(app.root_path, 'static', 'books')
    pdf_path = os.path.join(pdf_directory, pdf_filename)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        return True
    else:
        return False

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book_pdf(book_id):
    book = Book.query.get_or_404(book_id)
    pdf_path = url_for('static', filename='books/' + book.pdf, _external=True)
    return jsonify({"pdf_url": pdf_path})

@app.route('/add-book', methods=['POST'])
@jwt_required()
@admin_required
def add_book():
    name = request.form['name']
    pdf = request.files['pdf']
    authors = request.form['authors']
    section_id = request.form['section_id']
    pdf_filename = save_pdf(pdf)
    book = Book(name=name, pdf=pdf_filename, authors=authors, section_id=section_id)
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book added successfully"}), 201

@app.route('/update-book/<int:book_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get_or_404(book_id)
    book.name = data['name']
    book.authors = data['authors']
    book.section_id = int(data['section'])
    db.session.commit()
    return jsonify({"message": "Book updated successfully"}), 200

@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    delete_pdf(book.pdf)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

@app.route('/my-books', methods=['GET'])
@jwt_required()
def my_books():
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    pending_requests = user.book_requests
    issued_books = user.issued_books
    completed_books = user.completed_books
    return jsonify({
        "pending_requests": [{'id': req.id, 'book': {'name': req.book.name, 'authors': req.book.authors, 'section': req.book.section.name}, 'days_requested': req.days_requested, 'request_status': req.request_status} for req in pending_requests],
        "issued_books": [{'id': book.id, 'name': book.name, 'authors': book.authors, 'section': book.section.name} for book in issued_books],
        "completed_books": [{'id': book.id, 'name': book.name, 'authors': book.authors, 'section': book.section.name } for book in completed_books]
    })


@app.route('/request/<int:book_id>', methods=['POST'])
@jwt_required()
def request_book(book_id):
    data = request.get_json()
    user = User.query.get(data["user_id"])
    number_of_requests = BookRequest.query.filter_by(user_id=user.id).count()
    if number_of_requests >= 5:
        return jsonify({"message":'You already have 5 active requests. Please return some books or cancel pending requests.'}), 400
    else:
        days = int(data["days"])
        if days <= 0:
            return jsonify({"message": "Invalid number of days. Please try again."}), 400
        book_request = BookRequest(book_id=book_id, user_id=user.id, days_requested=days)
        db.session.add(book_request)
        db.session.commit()
        return jsonify({"message": "Book requested successfully"}), 201

@app.route('/book-requests', methods=['GET'])
@jwt_required()
@admin_required
def get_book_requests():
    book_requests = BookRequest.query.all()
    result = [
        {
            'id': req.id,
            'book': {'name': req.book.name, 'authors': req.book.authors},
            'requested_by': {'username': req.requested_by.username},
            'days_requested': req.days_requested,
            'request_status': req.request_status,
            'date_requested': req.date_requested
        }
        for req in book_requests
    ]
    return jsonify(result)

@app.route('/cancel-request/<int:book_request_id>', methods=['DELETE'])
@jwt_required()
def cancel_request(book_request_id):
    request = BookRequest.query.get_or_404(book_request_id)
    db.session.delete(request)
    db.session.commit()
    return jsonify({'message': 'Request cancelled successfully!'}), 200

@app.route('/reject-request/<int:book_request_id>', methods=['GET'])
@jwt_required()
@admin_required
def reject_request(book_request_id):
    request = BookRequest.query.get_or_404(book_request_id)
    db.session.delete(request)
    db.session.commit()
    return jsonify({'message': 'Request rejected successfully!'})

@app.route('/issue-book/<int:book_request_id>', methods=['GET'])
@jwt_required()
@admin_required
def issue_book(book_request_id):
    request = BookRequest.query.get_or_404(book_request_id)
    return_date = datetime.utcnow() + timedelta(days=request.days_requested)
    request.return_date = return_date
    request.request_status = 'issued'
    association = {
        'user_id': request.requested_by.id,
        'book_id': request.book.id,
        'date_issued': datetime.utcnow(),
        'return_date': return_date
    }
    db.session.execute(insert(user_books).values(association))
    db.session.commit()
    return jsonify({'message': 'Book issued successfully!'}), 200

@app.route('/revoke-book/<int:book_request_id>', methods=['GET'])
def revoke_book(book_request_id):
    request = BookRequest.query.get_or_404(book_request_id)
    user = User.query.get(request.requested_by.id)
    book = Book.query.get(request.book.id)
    user.issued_books.remove(book)
    db.session.delete(request)
    db.session.commit()
    return jsonify({'message': 'Book revoked successfully!'}), 200

@app.route('/return-book/<int:book_id>', methods=['POST'])
def return_book(book_id):
    data = request.get_json()
    user_id = data['user_id']
    user = User.query.get(user_id)
    book = Book.query.get(book_id)
    book_request = BookRequest.query.filter_by(book_id=book_id, user_id=user.id).first()
    feedback = Feedback(book_id=book_id, user_id=user_id, rating=data['rating'], review=data['review'])
    user.issued_books.remove(book)
    user.completed_books.append(book)
    db.session.delete(book_request)
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Book returned successfully!'}), 200

def generate_admin_pie_chart(sections):
    section_book_counts = {section.name: len(section.books) for section in sections if section.books}
    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(10, 7))
    plt.pie(section_book_counts.values(), labels=section_book_counts.keys(), autopct='%.2f%%', startangle=120, colors=sns.color_palette('muted'))
    plt.tight_layout()
    pie_chart_path = os.path.join(app.root_path, 'static', 'charts', 'admin_pie_chart.png')
    plt.savefig(pie_chart_path)
    plt.close()
    return pie_chart_path

def generate_admin_bar_chart(pending_count, issued_count, completed_count):
    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(10, 7))
    plt.bar(['Pending', 'Issued', 'Completed'], [pending_count, issued_count, completed_count], color=sns.color_palette('muted'))
    plt.tight_layout()
    bar_chart_path = os.path.join(app.root_path, 'static', 'charts', 'admin_bar_chart.png')
    plt.savefig(bar_chart_path)
    plt.close()
    return bar_chart_path

@app.route('/admin-dashboard', methods=['GET'])
@jwt_required()
@cache.cached(timeout=30)
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_books = Book.query.count()
    total_sections = Section.query.count()

    sections = Section.query.all()
    generate_admin_pie_chart(sections)

    pending_count = BookRequest.query.filter_by(request_status='pending').count()
    issued_count = BookRequest.query.filter_by(request_status='issued').count()
    completed_count = db.session.query(completed_books).count()
    generate_admin_bar_chart(pending_count, issued_count, completed_count)
    
    bar_chart_url = url_for('static', filename='charts/admin_bar_chart.png', _external=True)
    pie_chart_url = url_for('static', filename='charts/admin_pie_chart.png', _external=True)

    return jsonify({"bar_chart_url": bar_chart_url, "pie_chart_url": pie_chart_url, "total_users": total_users, "total_books": total_books, "total_sections": total_sections}), 200

def generate_user_pie_chart(completed_books):
    section_book_counts = {book.section.name: len(book.section.books) for book in completed_books}
    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(10, 7))
    plt.pie(section_book_counts.values(), labels=section_book_counts.keys(), autopct='%.2f%%', startangle=120, colors=sns.color_palette('muted'))
    plt.tight_layout()
    pie_chart_path = os.path.join(app.root_path, 'static', 'charts', 'user_pie_chart.png')
    plt.savefig(pie_chart_path)
    plt.close()
    return pie_chart_path    

def generate_user_bar_chart(pending_count, issued_count, completed_count):
    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(10, 7))
    plt.bar(['Pending', 'Issued', 'Completed'], [pending_count, issued_count, completed_count], color=sns.color_palette('muted'))
    plt.tight_layout()
    bar_chart_path = os.path.join(app.root_path, 'static', 'charts', 'user_bar_chart.png')
    plt.savefig(bar_chart_path)
    plt.close()
    return bar_chart_path

@app.route('/user-dashboard', methods=['GET'])
@jwt_required()
@cache.cached(timeout=30)
def user_dashboard():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    pending_count = BookRequest.query.filter_by(user_id=user_id, request_status='pending').count()
    issued_count = len(user.issued_books)
    completed_books = user.completed_books
    completed_count = len(completed_books)
    generate_user_pie_chart(completed_books)
    generate_user_bar_chart(pending_count, issued_count, completed_count)
    bar_chart_url = url_for('static', filename='charts/user_bar_chart.png', _external=True)
    pie_chart_url = url_for('static', filename='charts/user_pie_chart.png', _external=True)
    return jsonify({"bar_chart_url": bar_chart_url, "pie_chart_url": pie_chart_url}), 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    if user:
        return jsonify({'username': user.username, 'email': user.email, 'role': user.role}), 200
    else:
        return jsonify({'msg': 'User not found'}), 404

@app.route('/remainder-email', methods=['GET'])
def remainder_email():
    daily_remainder.delay()
    return jsonify({'msg': 'Email sent successfully'}), 200

@app.route('/monthly-report', methods=['GET'])
def monthly_report():
    monthly_activity_report.delay()
    return jsonify({'msg': 'Monthly report generated successfully'}), 200

@app.route('/export-csv', methods=['GET'])
def send_csv_file():
    task = generate_csv_file.delay()
    task.wait()
    file_path = task.result 
    return send_file(file_path, as_attachment=True, mimetype='text/csv')