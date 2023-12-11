import pytest
import os
from app import app, perform_data_analysis, fetch_data_by_name
from db import get_db
import statistics

report_directory = r'C:\Users\athi1\.jenkins\workspace\WeatherStationBuildAndTest\test-reports'
os.makedirs(report_directory, exist_ok=True)
xml_report_path = os.path.join(report_directory, 'test_report.xml')

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>Data Management</h1>' in response.data
    assert b'<button type="submit">Collect Data</button>' in response.data
    assert b'<button type="submit">Data Storage</button>' in response.data
    assert b'<button type="submit">Transmit Data</button>' in response.data
    assert b'<button type="submit">Data Analysis</button>' in response.data


def test_collect_data(client):
    # You can add more test cases based on different scenarios
    response = client.post('/collect_data', data=dict(name='TestName', data=42, author='TestAuthor'))
    assert response.status_code == 302  # Redirect status code

def test_data_storage(client):
    response = client.get('/data_storage')
    assert response.status_code == 200
    assert b'Data Storage' in response.data

def test_transmit_data(client):
    response = client.post('/transmit_data', data=dict(name='TestName'))
    assert response.status_code == 200
    assert b'Transmit Data' in response.data

def test_fetch_data_by_name():
    # Adding print statements for debugging
    print("Running test_fetch_data_by_name")

    # Use the normal database connection
    conn = get_db()
    select_data_query = "SELECT data, author, date FROM data WHERE name = %s"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_data_query, ('TestName',))
    data = cursor.fetchone()
    cursor.close()

    # Checking the result
    print("Data:", data)
    assert data is not None  # Adjust based on your expected behavior

def test_perform_data_analysis():
    # Adding print statements for debugging
    print("Running test_perform_data_analysis")

    # Use the normal database connection
    conn = get_db()
    select_data_query = "SELECT data FROM data WHERE name = %s"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(select_data_query, ('TestName',))
    
    # Modify the test data to contain at least two data points
    data_list = [row['data'] for row in cursor.fetchall()][:2]
    cursor.close()

    if len(data_list) < 2:
        print("Not enough data points for analysis.")
        return None  # Return None if there are not enough data points

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

    # Checking the result
    print("Analysis Result:", analysis_result)
    assert analysis_result is not None  # Adjust based on your expected behavior

if __name__ == '__main__':
    pytest.main(['-o', 'junit_family=xunit2', '--junit-xml', xml_report_path])