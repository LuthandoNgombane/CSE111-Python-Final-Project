#LN - import tinkter module to create GUI
import tkinter as tk

#LN - import messagebox and filedialog from tkinter module to display message box and file dialog
from tkinter import messagebox, filedialog

#LN - import requests module to fetch data from API
import requests

#LN - import pandas module to work with data in DataFrame format
import pandas as pd

#LN - import json_normalize from pandas module to normalize JSON data
from pandas import json_normalize

#LN - import mysql.connector module to connect to MySQL database
import mysql.connector

#LN - import matplotlib.pyplot module to visualize data
import matplotlib.pyplot as plt

#LN - import os module to work with file paths in the operating system
import os

#LN - import shutil module to move files to different directories
import shutil

#LN - import glob module to work with file paths using pattern matching
import glob

#LN - define fetch_api_data function to fetch weather data from OpenWeather API
def fetch_api_data(city_name: str) -> dict:
    
    """Fetches weather data using OpenWeather via RapidAPI."""
    
    #LN - define the endpoint URL
    url = "https://open-weather13.p.rapidapi.com/city/" + city_name + "/EN"

    #LN - define the headers for the API request
    headers = {
        "X-RapidAPI-Key": "d23ead87bamsh87a51f415f2e63ap15b15ajsndc5dd53b6b73", 
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }

    #LN - try to fetch data from the API
    try:
        
        #LN - send a GET request to the API
        response = requests.get(url, headers=headers)
        
        #LN - check for any errors in the response
        response.raise_for_status()
        
        #LN - return the JSON response
        return response.json()
    
    #LN - handle any exceptions during the API request
    except requests.exceptions.RequestException as e:
        
        #LN - display an error message if there is an issue with the API request
        messagebox.showerror("API Error", f"Error fetching data: {e}")
        
        #LN - return an empty dictionary if there is an error
        return {}
    

#LN - define process_data function to convert API data into a DataFrame
def process_data(data: dict) -> pd.DataFrame:
    
    """Converts API data into a DataFrame."""
    
    #LN - check if the data is empty
    if not data:
        
        #LN - return an empty DataFrame if the data is empty
        return pd.DataFrame()
    
    #LN - check if the data is a dictionary
    if isinstance(data, dict):
        
        #LN - flatten the JSON data into a DataFrame
        df = pd.json_normalize(data)
        
    #LN - check if the data is a list
    elif isinstance(data, list):
        
        #LN - normalize the JSON data into a DataFrame
        df = pd.DataFrame(data)
        
    #LN - return an empty DataFrame if the data structure is unexpected
    else:

        #LN - return any DataFrame if the data structure is unexpected
        df = pd.DataFrame()

    return df


#LN - define store_data_in_mysql function to store weather data in MySQL database
def store_data_in_mysql(data: dict, table_name: str):
    
    """Stores only the displayed weather data in MySQL."""
    
    #LN - try to connect to the MySQL database
    try:
        
        #LN - establish a connection to the MySQL database
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='test')
        
        #LN - create a cursor to execute SQL queries
        cursor = conn.cursor()

        #LN - create a table if it does not exist
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                location VARCHAR(255),
                temperature FLOAT,
                feels_like FLOAT,
                weather_condition VARCHAR(255),
                wind_speed FLOAT,
                wind_direction FLOAT,
                wind_gusts FLOAT,
                humidity INT,
                pressure INT,
                visibility INT,
                sunrise DATETIME,
                sunset DATETIME
            )
        """
        
        #LN - execute the create table query
        cursor.execute(create_table_query)

        #LN - insert the weather data into the table
        insert_query = f"""
            INSERT INTO {table_name} (
                location, temperature, feels_like, weather_condition,
                wind_speed, wind_direction, wind_gusts,
                humidity, pressure, visibility, sunrise, sunset
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            f"{data.get('name')}, {data['sys'].get('country')}",
            data['main'].get('temp'),
            data['main'].get('feels_like'),
            data['weather'][0].get('description').capitalize(),
            data['wind'].get('speed'),
            data['wind'].get('deg'),
            data['wind'].get('gust'),
            data['main'].get('humidity'),
            data['main'].get('pressure'),
            data.get('visibility'),
            pd.to_datetime(data['sys'].get('sunrise'), unit='s').strftime('%Y-%m-%d %H:%M:%S'),
            pd.to_datetime(data['sys'].get('sunset'), unit='s').strftime('%Y-%m-%d %H:%M:%S')
        )

        #LN - execute the insert query with the weather data values
        cursor.execute(insert_query, values)

        #LN - commit the changes to the database
        conn.commit()
        
        #LN - create a CSV file with the weather data
        pd.DataFrame([data]).to_csv(f"{data.get('name')}_weather.csv", index=False)
    
        #LN - close the database connection
        conn.close()
        
        #LN - display a success message if the data is stored successfully
        messagebox.showinfo("Success", "Weather data stored and CSV created!")
        
    #LN - handle any exceptions during the database operations
    except mysql.connector.Error as e:
        
        #LN - display an error message if there is an issue with the database
        messagebox.showerror("Database Error", f"Error storing data: {e}")


#LN - define visualize_data function to display a weather statistics chart
def visualize_data():
    
    """Fetches data from MySQL and displays a weather statistics chart."""
    
    #LN - try to connect to the MySQL database
    try:
        
        #LN - establish a connection to the MySQL database
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='test')
        
        #LN - query to fetch weather data from the database
        query = "SELECT temperature, humidity, wind_speed, pressure FROM weather_data"
        
        #LN - read the data from the database into a DataFrame
        df = pd.read_sql(query, conn)
        
        #LN - close the database connection
        conn.close()

        #LN - check if the DataFrame is empty
        if df.empty:
            
            #LN - display a warning message if there is no data available
            messagebox.showwarning("Warning", "No data available for visualization.")
            
            #LN - return from the function
            return

        #LN - create a figure for the chart
        plt.figure(figsize=(10, 6))
        
        #LN - plot the weather statistics on the chart
        plt.plot(df.index, df['temperature'], label='Temperature (°F)', marker='o')
        plt.plot(df.index, df['humidity'], label='Humidity (%)', marker='s')
        plt.plot(df.index, df['wind_speed'], label='Wind Speed (m/s)', marker='^')
        plt.plot(df.index, df['pressure'], label='Pressure (hPa)', marker='x')
        plt.title("Weather Statistics")
        plt.xlabel("Record Number")
        plt.ylabel("Values")
        plt.legend()
        plt.grid(True)
        plt.show()

    #LN - handle any exceptions during the database operations
    except Exception as e:
        
        #LN - display an error message if there is an issue with the visualization
        messagebox.showerror("Visualization Error", f"Error generating chart: {e}")

#LN - define tidy_up_files function to rename and organize files in a directory
def tidy_up_files():
    
    """Prompts the user for a directory, then renames and organizes files."""
    
    #LN - prompt the user to select a directory
    directory = filedialog.askdirectory(title="Select Directory to Organize")
    
    #LN - check if the user selected a directory
    if not directory:
        return

    #LN - rename files in the selected directory
    rename_files(directory, "*.csv")
    
    #LN - organize files by their types in the directory
    organize_files_by_type(directory)
    
    #LN - display a success message after renaming and organizing files
    messagebox.showinfo("Success", "Files have been renamed and organized.")

#LN - define rename_files function to rename files in a directory
def rename_files(directory: str, pattern: str):
    
    """Renames files in a specified directory."""
    
    #LN - get a list of files that match the pattern in the directory
    files = glob.glob(f"{directory}/{pattern}")
    
    #LN - iterate over the files and rename them
    for idx, file in enumerate(files, 1):
        
        #LN - get the file extension
        ext = os.path.splitext(file)[1]
        
        #LN - rename the file with a new name
        os.rename(file, os.path.join(directory, f"file_{idx}{ext}"))
        
#LN - define organize_files_by_type function to organize files by their types
def organize_files_by_type(directory: str):
    
    """Moves files into folders based on their file types."""
    
    #LN - iterate over the files in the directory
    for file in os.listdir(directory):
        
        #LN - get the full path of the file
        file_path = os.path.join(directory, file)
        
        #LN - check if the file is a regular file
        if os.path.isfile(file_path):
            
            #LN - get the file extension
            ext = file.split('.')[-1]
            
            #LN - create a target directory based on the file extension
            target_dir = os.path.join(directory, ext)
            
            #LN - create the target directory if it does not exist
            os.makedirs(target_dir, exist_ok=True)
            
            #LN - move the file to the target directory
            shutil.move(file_path, os.path.join(target_dir, file))

#LN - define setup_gui function to create the main GUI window
def setup_gui():

    """Sets up the main GUI window for the Data Manager."""
    
    #LN - create the main GUI window
    root = tk.Tk()
    
    #LN - set the title of the window
    root.title("Data Manager")
    
    #LN - set the size of the window
    root.geometry("400x300")

    #LN - create a label for the city name input
    city_label = tk.Label(root, text="City Name:")
    
    #LN - display the city label
    city_label.pack()

    #LN - create an entry field for the city name
    city_entry = tk.Entry(root, width=50)
    
    #LN - display the city entry field
    city_entry.pack()
    
    #LN - define the fetch_data function to fetch weather data
    def fetch_data():
        
        """Fetches weather data for the specified city."""
        
        # LN - get the city name from the entry field
        city = city_entry.get()
        
        #LN - fetch weather data for the specified city
        data = fetch_api_data(city)
        
        #LN - process the weather data into a DataFrame
        df = process_data(data)
        
        #LN - check if the DataFrame is not empty
        if not df.empty:
            
            #LN - display the weather summary and used wind + . for emojies, learnt this is WDD130
            try:
                
                weather_summary = (
                    f"📍 Location: {data.get('name')}, {data['sys'].get('country')}\n"
                    f"🌡️ Temperature: {data['main'].get('temp')} °F (Feels like: {data['main'].get('feels_like')} °F)\n"
                    f"☁️ Condition: {data['weather'][0].get('description').capitalize()}\n"
                    f"💨 Wind: {data['wind'].get('speed')} m/s, Direction: {data['wind'].get('deg')}°\n"
                    f"🌬️ Gusts: {data['wind'].get('gust')} m/s\n"
                    f"☂️ Humidity: {data['main'].get('humidity')}%\n"
                    f"📊 Pressure: {data['main'].get('pressure')} hPa\n"
                    f"👁️ Visibility: {data.get('visibility')} meters\n"
                    f"🌞 Sunrise: {pd.to_datetime(data['sys'].get('sunrise'), unit='s')}\n"
                    f"🌙 Sunset: {pd.to_datetime(data['sys'].get('sunset'), unit='s')}\n"
                )
                
                messagebox.showinfo("Weather Summary", weather_summary)

                #LN - store the weather data in the MySQL database
                store_data_in_mysql(data, table_name="weather_data")

            #LN - handle any exceptions during the weather summary display
            except Exception as e:
                
                #LN - display an error message if there is an issue with the weather summary
                messagebox.showerror("Parsing Error", f"Error extracting weather summary: {e}")
                
        #LN - display a warning if there is no data to store
        else:
            
            messagebox.showwarning("Warning", "No data to store.")

    #LN - create a button to fetch weather data    
    fetch_button = tk.Button(root, text="Fetch Weather Data", command=fetch_data)
    fetch_button.pack(pady=5)

    #LN - create a button to tidy up files
    tidy_button = tk.Button(root, text="Tidy Up Files", command=tidy_up_files)
    tidy_button.pack(pady=5)

    #LN - create a button to visualize weather data
    visualize_button = tk.Button(root, text="Visualize Weather Data", command=visualize_data)
    visualize_button.pack(pady=5)

    #LN - run the main GUI window
    root.mainloop()

#LN - check if the script is run as the main program
if __name__ == "__main__":
    setup_gui() 
    # print(process_data(fetch_api_data("London")))
    # print(store_data_in_mysql(fetch_api_data("London"), "weather_data"))
    # print(visualize_data())
    # print("Running Weather Data App")
