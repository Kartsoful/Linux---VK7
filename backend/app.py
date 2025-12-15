from flask import Flask, jsonify, request
import os
import mysql.connector
import requests

# Flask app instance
app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme')
DB_NAME = os.getenv('DB_NAME', 'appdb')
OWM_API_KEY = os.getenv('OWM_API_KEY')  # OpenWeatherMap API key

@app.get('/api/health')
def health():
    return jsonify(message={'status': 'ok'})

@app.get('/api/time')
def time():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message={'time': row[0]})

@app.get('/api')
def index():
    """Simple endpoint that greets from DB."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Morjes backendin tietokannasta!'")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message=row[0])

@app.get('/api/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify(message="Anna kunta-parametri city"), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OWM_API_KEY}"
    resp = requests.get(url)
    
    if resp.status_code != 200:
        return jsonify(message=f"Kuntaa '{city}' ei löydy API-rajapinnan takaa"), 404

    data = resp.json()
    temp = data['main']['temp']
    return jsonify(message=f"{city}-kunnan lämpötila on {temp} °C")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
