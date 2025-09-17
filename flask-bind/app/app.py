from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = "/data"
VISITS_FILE = os.path.join(DATA_DIR, "visits.json")

def init_data():
    """Инициализация файла данных, если его нет"""
    if not os.path.exists(VISITS_FILE):
        data = {
            "total_visits": 0,
            "last_visit": None,
            "visit_history": []
        }
        save_data(data)

def load_data():
    """Загрузка данных из файла"""
    try:
        with open(VISITS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"total_visits": 0, "last_visit": None, "visit_history": []}

def save_data(data):
    """Сохранение данных в файл"""
    with open(VISITS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    """Главная страница - увеличивает счетчик посещений"""
    data = load_data()
    
    data["total_visits"] += 1
    now = datetime.now().isoformat()
    data["last_visit"] = now
    data["visit_history"].append(now)
    
    save_data(data)
    
    return render_template('index.html', 
                         visits=data["total_visits"], 
                         last_visit=data["last_visit"])

@app.route('/api/stats')
def stats():
    """API endpoint для получения статистики"""
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    init_data()
    
    app.run(host='0.0.0.0', port=5000, debug=True)