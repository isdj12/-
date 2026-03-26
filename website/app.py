from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# HTML шаблон главной страницы
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тестовый сайт</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        button { padding: 10px 20px; margin: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🧪 Тестовый сайт для AI-МОЗГ</h1>
    <div class="status success">✅ Сайт работает нормально</div>
    
    <h2>API Endpoints:</h2>
    <ul>
        <li><a href="/api/status">/api/status</a> - статус сервера</li>
        <li><a href="/api/users">/api/users</a> - список пользователей</li>
        <li><a href="/api/data">/api/data</a> - тестовые данные</li>
        <li><a href="/api/error">/api/error</a> - тест ошибки 500</li>
    </ul>
    
    <h2>Тестовые кнопки:</h2>
    <button onclick="testAPI('/api/status')">Проверить статус</button>
    <button onclick="testAPI('/api/users')">Получить пользователей</button>
    <button onclick="testAPI('/api/data')">Получить данные</button>
    
    <div id="result"></div>
    
    <script>
        function testAPI(url) {
            fetch(url)
                .then(r => r.json())
                .then(data => {
                    document.getElementById('result').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                })
                .catch(err => {
                    document.getElementById('result').innerHTML = 
                        '<div class="status error">Ошибка: ' + err + '</div>';
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'ok',
        'message': 'Сервер работает',
        'version': '1.0.0'
    })

@app.route('/api/users')
def api_users():
    return jsonify({
        'users': [
            {'id': 1, 'name': 'Иван', 'email': 'ivan@test.ru'},
            {'id': 2, 'name': 'Мария', 'email': 'maria@test.ru'},
            {'id': 3, 'name': 'Петр', 'email': 'petr@test.ru'}
        ]
    })

@app.route('/api/data')
def api_data():
    return jsonify({
        'data': {
            'temperature': 22.5,
            'humidity': 65,
            'timestamp': '2026-03-05T12:00:00'
        }
    })

@app.route('/api/error')
def api_error():
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    print("🌐 Тестовый сайт запущен на http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
