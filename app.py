from flask import Flask, render_template, request, redirect, url_for
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Получаем значения из переменных окружения, добавляем значения по умолчанию
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8133198843:AAE_DLqJpK3k_O0MuyLSs_90lhWQG8x8H_k")
CHAT_ID = os.getenv("CHAT_ID", "1121729925")

# Данные для отправки email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "politime.ua@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "gifq knqx ogjh ckdq")
SUBJECT = "Новая оплата"

# Пример товаров
products = {
    'start_subscription': {'name': 'START 30д', 'price': 19},
    'meteor_subscription': {'name': 'METEOR 30д', 'price': 35},
    'guardian_subscription': {'name': 'GUARDIAN 30д', 'price': 49},
    'paladin_subscription': {'name': 'PALADIN 30д', 'price': 79},
    'neo_subscription': {'name': 'NEO 30д', 'price': 149},
    'moon_subscription': {'name': 'MOON 30д', 'price': 239},
    'magister_subscription': {'name': 'MAGISTER 30д', 'price': 539},
    'rocket_subscription': {'name': 'ROCKET 30д', 'price': 749},
    'donate_case': {'name': 'Донат Кейс', 'price': 59},
    'title_case': {'name': 'Кейс из титула', 'price': 19},
    'coin_case': {'name': 'Кейс из монет', 'price': 29},
    'shard_case': {'name': 'Кейс из осколков', 'price': 59},
    'battle_pass': {'name': 'Боевой Пропуск', 'price': 89},
    'unban': {'name': 'Разбан', 'price': 222},
    'shards': {'name': 'Осколки (пакет)', 'price': 39},
}

# Функция для отправки email
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"Email отправлен на {to_email}")
    except Exception as e:
        print(f"Ошибка при отправке email: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/pay/<product_id>', methods=['GET', 'POST'])
def pay(product_id):
    product = products.get(product_id)
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        comment = request.form.get('comment', '')
        transaction_code = request.form.get('transaction_code', '')

        # Создаем сообщение для Telegram
        message = f"Новая оплата:\n\nПродукт: {product['name']}\nЦена: {product['price']} грн\nНик: {username}\nКомментарий: {comment}\nEmail: {email}\nКод транзакции: {transaction_code}"

        # Отправляем сообщение в Telegram
        try:
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            params = {
                'chat_id': CHAT_ID,
                'text': message
            }
            response = requests.get(telegram_url, params=params)
            response.raise_for_status()  # Проверяем успешность запроса
            print("Сообщение отправлено в Telegram")
        except Exception as e:
            print(f"Ошибка при отправке сообщения в Telegram: {str(e)}")

        # Формируем текст письма для email
        email_body = f"Новая оплата:\n\nПродукт: {product['name']}\nЦена: {product['price']} грн\nНик: {username}\nКомментарий: {comment}\nEmail: {email}\nКод транзакции: {transaction_code}"

        # Отправка email
        send_email(email, SUBJECT, email_body)

        return redirect(url_for('payment_confirmed', product_name=product['name'], price=product['price'], username=username, comment=comment, email=email, transaction_code=transaction_code))

    return render_template('pay.html', product=product)

@app.route('/payment_confirmed')
def payment_confirmed():
    product_name = request.args.get('product_name')
    price = request.args.get('price')
    username = request.args.get('username')
    comment = request.args.get('comment')
    email = request.args.get('email')
    transaction_code = request.args.get('transaction_code')

    return render_template('payment_confirmed.html', product_name=product_name, price=price, username=username, comment=comment, email=email, transaction_code=transaction_code)

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)
