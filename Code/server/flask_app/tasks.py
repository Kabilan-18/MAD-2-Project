from celery import shared_task
from flask import render_template
from flask_app import celery, db
from flask_app.models import User, Section, Book, BookRequest, Feedback
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
import os


email = os.environ.get('EMAIL_ADDRESS')
password = os.environ.get('APP_PASSWORD')

def send_remainder_email(to_email):
    msg = EmailMessage()
    msg['From'] = email
    msg['To'] = to_email
    msg['Subject'] = 'BookHub : Remainder'
    msg.set_content('This is a reminder to return the book you borrowed from BookHub.')

    with smtplib.SMTP_SSL('smtp.gmail.com') as server:
        server.login(email, password)
        server.send_message(msg)


@shared_task()
def daily_remainder():
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    
    users_with_reminders = db.session.query(User).join(BookRequest).filter(
        (BookRequest.return_date <= tomorrow) |
        (BookRequest.return_date == now)
    ).all()

    for user in users_with_reminders:
        send_remainder_email(user.email)

def send_monthly_activity_report(report):
    msg = EmailMessage()
    msg['From'] = email
    librarian_user = User.query.filter_by(role='librarian').first()
    msg['To'] = '22f2000945@ds.study.iitm.ac.in'
    msg['Subject'] = 'BookHub : Monthly Activity Report'
    msg.add_attachment(report, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com') as server:
        server.login(email, password)
        server.send_message(msg)

@shared_task()
def monthly_activity_report():
    now = datetime.utcnow()
    start_of_last_month = now - timedelta(days=30)

    sections = Section.query.all()
    books = Book.query.all()
    feedbacks = Feedback.query.filter(Feedback.date_posted.between(start_of_last_month, now)).all()
    book_requests = BookRequest.query.filter(BookRequest.date_requested.between(start_of_last_month, now)).all()
    
    report_html = render_template('monthly_report.html', sections=sections, books=books, feedbacks=feedbacks, book_requests=book_requests)
    send_monthly_activity_report(report_html)


@shared_task()
def generate_csv_file():
    book_requests = BookRequest.query.all()
    path = os.path.join(os.getcwd(), 'flask_app', 'static', 'requests.csv')
    with open(path, 'w') as file:
        file.write('Book Request ID, Book, User, Request Status , Date Requested, Return Date\n')
        for request in book_requests:
            username = User.query.get(request.user_id).username
            book_name = Book.query.get(request.book_id).name
            file.write(f'{request.id}, {book_name}, {username}, {request.request_status}, {request.date_requested}, {request.return_date}\n')
    return path