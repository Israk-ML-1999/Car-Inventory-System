# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('car_inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    cars = cursor.fetchall()
    conn.close()
    return render_template('index.html', cars=cars)

@app.route('/add_car', methods=['POST'])
def add_car():
    name = request.form['name']
    model = request.form['model']
    year = request.form['year']
    car_type = request.form['car_type']
    
    if car_type == 'Electric':
        battery_capacity = request.form['battery_capacity']
        save_car(name, model, year, car_type, battery_capacity)
    elif car_type == 'Gas':
        fuel_efficiency = request.form['fuel_efficiency']
        save_car(name, model, year, car_type, fuel_efficiency)

    return redirect(url_for('index'))

def save_car(name, model, year, car_type, additional_info):
    conn = sqlite3.connect('car_inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cars (name, model, year, type, additional_info)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, model, year, car_type, additional_info))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
