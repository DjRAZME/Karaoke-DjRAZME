from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Список песен DjRAZME
songs_db = ["The Carpathian Mantra", "Modern Techno Mix", "Ukrainian Folk Remix", "DjRAZME Special"]
orders = []

@app.route('/')
def index():
    return render_template('index.html', songs=songs_db)

@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    song = data.get('song')
    if song:
        orders.append(song)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/admin_panel')
def admin():
    # Простая страница для тебя, чтобы видеть заказы
    html = "<h1>Заказы DjRAZME:</h1><ul>"
    for o in orders:
        html += f"<li>{o}</li>"
    html += "</ul><script>setTimeout(function(){location.reload();}, 3000);</script>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
