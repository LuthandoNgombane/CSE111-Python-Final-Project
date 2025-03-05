#LN - Import the necessary libraries
import os
import mysql.connector
import pandas as pd
from data_manage_gui import fetch_api_data, process_data, store_data_in_mysql

# LN - Test the fetch_api_data function
def test_fetch_api_data():
    
    """Verify that the fetch_api_data function works correctly."""
    
    # LN - Ensure the function runs without errors
    assert isinstance(fetch_api_data("London"), dict), "Should return a dictionary"
    assert "weather" in fetch_api_data("London"), "Should contain weather information"
    assert "main" in fetch_api_data("New York"), "Should contain main weather details"
    assert "name" in fetch_api_data("Paris"), "Should contain city name"
   
# LN - Test the process_data function
def test_process_data():
    
    """Verify that the process_data function works correctly."""
    
    # LN - Fetch data from the API and process it
    df = process_data(fetch_api_data("London"))
    
    # LN - Ensure the function runs without errors
    assert isinstance(df, pd.DataFrame), "Should return a pandas DataFrame"
    assert not df.empty, "DataFrame should not be empty"
    assert "weather" in df.columns, "DataFrame should contain a 'weather' column"
    assert "base" in df.columns, "DataFrame should contain a 'base' column"
    assert "sys.country" in df.columns, "DataFrame should contain a 'sys.country' column"
    

# LN - Test the store_data_in_mysql function
def test_store_data_in_mysql():
    """Verify that store_data_in_mysql inserts data into MySQL and creates a CSV file."""
    
    # LN - Define the table name and city
    table_name = "weather_data"
    city = "London"
    
    # LN - Fetch data from the API
    data = fetch_api_data(city)
    
    # LN - Ensure the function runs without errors
    store_data_in_mysql(data, table_name)
    
    # LN - Verify data exists in MySQL
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='test')
    cursor = conn.cursor(buffered=True)  # Use buffered=True to prevent unread result issues
    
    # LN - Execute the SELECT query first
    cursor.execute(f"SELECT * FROM {table_name} WHERE location LIKE '{city}%'")
    result = cursor.fetchone()  # Fetch one result
    
    assert result is not None, "Data should be inserted into the database"
    
    # LN - Verify that the CSV file is created
    csv_filename = f"{city}_weather.csv"
    assert os.path.exists(csv_filename), "CSV file should be created"
    
    # LN - Delete the data from MySQL and remove the CSV file for ease of testing
    cursor.execute(f"DELETE FROM {table_name} WHERE location LIKE '{city}%'")
    conn.commit()
    
    # LN - Close database connection
    cursor.close()
    conn.close()
    
    # LN - Remove the CSV file
    os.remove(csv_filename)


# LN - Run the tests
if __name__ == "__main__":
    print("Running tests...")
    # test_fetch_api_data()
    # test_process_data()
    test_store_data_in_mysql()
    print("All tests passed!")
