import os
import sys
import pandas as pd
from db_analysis_utilities import *
def get_actuator_df(config_id, actuator_names):
    db = DatabaseInstance()
    db.establishConnection()
    actuators = db.values_actuators(actuator_names, config_id)
    df = pd.DataFrame()
    for actuator in actuators:
        df[actuator] = actuators[actuator]["value"]
    df.index = actuators[actuator_names[0]]["timestamp"]
    return df
def get_sensor_df(config_id, sensor_names):
    db = DatabaseInstance()
    db.establishConnection()
    sensors = db.values_sensors(sensor_names, config_id)
    df = pd.DataFrame()
    for sensor in sensors:
        df[sensor] = sensors[sensor]["value"]
    df.index = sensors[sensor_names[0]]["timestamp"]
    return df
def save_df_to_csv(df, filename):
    subfolder_name = "raw_data"

    # Get the parent folder path
    parent_folder = os.path.dirname(os.path.abspath(__file__))

    # Create the subfolder if it doesn't exist
    subfolder_path = os.path.join(parent_folder,"r_analysis",subfolder_name)
    if not os.path.exists(subfolder_path):
        print(subfolder_path, "does not exist! Stopping...")
        sys.exit(1)

    # Save the DataFrame to the CSV file in the  subfolder
    df.to_csv(os.path.join(subfolder_path, filename), index = False)


if __name__ == "__main__":
    data_type = input("Do you want sensor data or actuator data? (sensor/actuator): ")
    if data_type.lower() == "sensor":
        config_id = int(input("Enter the config_id: "))
        sensor_names = input("Enter the sensor names (comma separated): ").split(',')
        sensor_names = [s.strip() for s in sensor_names]
        df = get_sensor_df(config_id, sensor_names)
    elif data_type.lower() == "actuator":
        config_id = int(input("Enter the config_id: "))
        actuator_names = input("Enter the actuator names (comma separated): ").split(',')
        actuator_names = [s.strip() for s in actuator_names]
        df = get_actuator_df(config_id, actuator_names)
    else:
        print("Invalid input! Stopping...")
        sys.exit(1)
    filename = f"{data_type}_{config_id}.csv"
    save_df_to_csv(df, filename)
