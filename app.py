from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Память для кнопки
app_config = {"orders_enabled": True}
orders = []

@app.route('/')
def index():
    try:
        if not app_config["orders_enabled"]:
            return "<h1 style='text-align:center;'>Караоке закінчено!</h1>", 200
        songs_db = ["The Carpathian Mantra", "Modern Techno Mix", "Ukrainian Folk Remix"]
        return render_template('index.html', songs=songs_db)
    except Exception as e:
        return f"Помилка в index.html: {str(e)}", 500

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    song = data.get('song')
    if song:
        orders.append(song)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/admin_panel')
def admin():
    try:
        return render_template('admin.html', orders=orders, enabled=app_config["orders_enabled"])
    except Exception as e:
        return f"Помилка в admin.html: {str(e)}", 500

@app.route('/toggle_orders', methods=['POST'])
def toggle():
    app_config["orders_enabled"] = not app_config["orders_enabled"]
    return jsonify({"status": "success", "enabled": app_config["orders_enabled"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
