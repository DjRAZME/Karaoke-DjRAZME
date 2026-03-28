from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

app_config = {"orders_enabled": True}
orders = []

@app.route('/')
def index():
    if not app_config["orders_enabled"]:
        return "<h1 style='text-align:center; padding-top:50px; font-family:sans-serif;'>Дякуємо! Караоке закінчено. До зустрічі!</h1>", 200
    
    # Считываем номер стола из ссылки
    table_num = request.args.get('table', '??') 
    
    songs_db = ["The Carpathian Mantra", "Modern Techno Mix", "Ukrainian Folk Remix", "DjRAZME Special"]
    return render_template('index.html', songs=songs_db, table=table_num)

@app.route('/order', methods=['POST'])
def order():
    if not app_config["orders_enabled"]:
        return jsonify({"status": "error"}), 403
    
    data = request.json
    song = data.get('song')
    table = data.get('table', '??') # Принимаем стол
    
    if song:
        orders.append({"song": song, "table": table}) # Сохраняем стол
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
