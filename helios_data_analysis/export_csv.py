import os
import sys
import pandas as pd
from db_analysis_utilities import *
def get_actuator_df(config_id, actuator_names):
    # Create a new DatabaseInstance
    with DatabaseInstance() as db:
        # Fetch the data for the specified actuators
        actuators = db.values_actuators(actuator_names, config_id)
    # Return the DataFrame
    return actuators
def get_sensor_df(config_id, sensor_names):
    # Create a new DatabaseInstance
    with DatabaseInstance() as db:
        # Fetch the data for the specified sensors
        sensors = db.values_sensors(sensor_names, config_id)
    # Return the DataFrame
    return sensors

def get_state_df(config_id):
    # Create a new Database Instance
    with DatabaseInstance() as db:
        # Fetch the data
        states = db.values_states(config_id)
    return states


def test_date(config_id):
    with DatabaseInstance() as db:
        return db.get_test_date(config_id)


def save_df_to_csv(df, filename):
    subfolder_name = "raw_data"

    # Get the parent folder path
    parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subfolder_path = os.path.join(parent_folder,"r_analysis", subfolder_name)
    if not os.path.exists(subfolder_path):
        print(subfolder_path, "does not exist! Stopping...")
        sys.exit(1)

    # Save the DataFrame to the CSV file in the  subfolder
    df.to_csv(os.path.join(subfolder_path, filename), index = False)




if __name__ == "__main__":
    # Ask the user if they want sensor data or actuator data
    data_type = input("Do you want sensor data or actuator data? (sensor/actuator/states): ")
    
    # Check if the user typed sensor or actuator
    if data_type.lower() == "sensor":
        # Ask the user for the config_id (the id of the test)
        config_id = int(input("Enter the config_id: "))
        
        # Ask the user for the sensor names (comma separated)
        sensor_names = input("Enter the sensor names (comma separated): ").split(',')
        
        # Remove any leading or trailing whitespace from the sensor names
        sensor_names = [s.strip() for s in sensor_names]
        
        # Get the sensor data from the database
        df = get_sensor_df(config_id, sensor_names)
    elif data_type.lower() == "actuator":
        # Ask the user for the config_id (the id of the test)
        config_id = int(input("Enter the config_id: "))
        
        # Ask the user for the actuator names (comma separated)
        actuator_names = input("Enter the actuator names (comma separated): ").split(',')
        
        # Remove any leading or trailing whitespace from the actuator names
        actuator_names = [s.strip() for s in actuator_names]
        
        # Get the actuator data from the database
        df = get_actuator_df(config_id, actuator_names)
    elif data_type.lower() == "states":
        # Ask the user for the config_id (the id of the test)
        config_id = int(input("Enter the config_id: "))
        
        # Get the state data from the database
        df = get_state_df(config_id)
    else:
        print("Invalid input! Stopping...")
        sys.exit(1)
    
    # Create a filename based on the data type, config_id, and test date
    filename = f"{data_type}_{config_id}_{test_date(config_id)}.csv"
    
    # Reset the index of the DataFrame to make it easier to read
    df.reset_index(inplace=True)  
    
    # Save the DataFrame to the CSV file
    save_df_to_csv(df, filename)

