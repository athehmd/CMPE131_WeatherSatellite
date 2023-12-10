import mariadb
import os
import requests
import statistics
from db import get_db
from flask import Flask, request, render_template, redirect, url_for, jsonify

#Initialize Flask app
app = Flask(__name__)

# Connector to the database
conn = get_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/collect_data', methods=['GET', 'POST'])
def collect_data():
    if request.method == 'POST':
        name = request.form.get('name')
        data = request.form.get('data')
        author = request.form.get('author')
        insert_data = "INSERT INTO data VALUES (%s, %s, %s, NOW())"
        data_credentials = (name, data, author)
        # execute and commit
        cursor = conn.cursor()
        cursor.execute(insert_data, data_credentials)
        cursor.close()
        conn.commit()
        return redirect(url_for('collect_data'))
    return render_template('collect_data.html')

@app.route('/data_storage', methods=['GET', 'POST'])
def data_storage():
    select_all_data_query = "SELECT * FROM data"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_all_data_query)
    data_list = cursor.fetchall()
    cursor.close()
    print("Data List:", data_list)  # Add this line for debugging
    return render_template('data_storage.html', data_list=data_list)

@app.route('/transmit_data', methods=['GET', 'POST'])
def transmit_data():
    if request.method == 'POST':
        name = request.form.get('name')
        data = fetch_data_by_name(name)
        return render_template('transmit_data.html', data=data, name=name)
    return render_template('transmit_data.html', data=None, name=None)

def fetch_data_by_name(name):
    select_data_query = "SELECT data, author, date FROM data WHERE name = %s"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_data_query, (name,))
    data = cursor.fetchone()
    cursor.close()
    return data

@app.route('/data_analysis', methods=['GET', 'POST'])
def data_analysis():
    if request.method == 'POST':
        name = request.form.get('name')
        analysis_result = perform_data_analysis(name)
        return render_template('data_analysis.html', analysis_result=analysis_result, name=name)
    return render_template('data_analysis.html', analysis_result=None, name=None)

def perform_data_analysis(name):
    select_data_query = "SELECT data FROM data WHERE name = %s"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_data_query, (name,))
    data_list = [row['data'] for row in cursor.fetchall()]
    cursor.close()
    if not data_list:
        return None  # Return None if no data is found for the given name
    # Calculate the necessary statistics
    average_value = statistics.mean(data_list)
    standard_deviation_value = round(statistics.stdev(data_list), 3)
    high_value = max(data_list)
    low_value = min(data_list)
    analysis_result = {
        'average': average_value,
        'standard_deviation': standard_deviation_value,
        'high': high_value,
        'low': low_value
    }
    return analysis_result

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    conn.close()
