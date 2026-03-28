from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Память сервера для кнопки: True - включено, False - выключено
app_config = {"orders_enabled": True}
orders = []

@app.route('/')
def index():
    # Если ты выключил заказы в админке, люди увидят это сообщение:
    if not app_config["orders_enabled"]:
        return "<h1 style='text-align:center; padding-top:50px; font-family:sans-serif;'>Дякуємо! Караоке закінчено. До зустрічі!</h1>", 200
    
    # Твой актуальный список песен:
    songs_db = ["The Carpathian Mantra", "Modern Techno Mix", "Ukrainian Folk Remix", "DjRAZME Special"]
    return render_template('index.html', songs=songs_db)

@app.route('/order', methods=['POST'])
def order():
    if not app_config["orders_enabled"]:
        return jsonify({"status": "error", "message": "Closed"}), 403
    
    data = request.json
    song = data.get('song')
    if song:
        orders.append(song)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/admin_panel')
def admin():
    # Передаем список заказов и статус кнопки в твой пульт управления
    return render_template('admin.html', orders=orders, enabled=app_config["orders_enabled"])

@app.route('/toggle_orders', methods=['POST'])
def toggle():
    # Эта функция меняет статус True на False и наоборот при нажатии кнопки
    app_config["orders_enabled"] = not app_config["orders_enabled"]
    return jsonify({"status": "success", "enabled": app_config["orders_enabled"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
