from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Память сервера: True - работает, False - выключено
app_config = {"orders_enabled": True}
orders = []

@app.route('/')
def index():
    if not app_config["orders_enabled"]:
        return "<h1 style='text-align:center; padding-top:50px;'>Дякуємо! Караоке закінчено. До зустрічі!</h1>", 200
    
    # Твой список песен (можешь менять названия здесь)
    songs_db = ["The Carpathian Mantra", "Modern Techno Mix", "Ukrainian Folk Remix"]
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
    return render_template('admin.html', orders=orders, enabled=app_config["orders_enabled"])

@app.route('/toggle_orders', methods=['POST'])
def toggle():
    app_config["orders_enabled"] = not app_config["orders_enabled"]
    return jsonify({"status": "success", "enabled": app_config["orders_enabled"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
