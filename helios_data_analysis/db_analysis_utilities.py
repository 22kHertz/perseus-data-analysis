import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import math
import matplotlib.pyplot as plt

pd.options.plotting.backend = "plotly"
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"
import mysql.connector as con
import os.path
import json
import sys


class DatabaseInstance:

    ## Basic connection methods
    def __init__(self):
        self.connection = None
        self.hostip = "perseus.vsos.ethz.ch"
        self.cursor = None
        self.tables = None

    def __enter__(self):
        self.connection, self.cursor = self.establishConnection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def establishConnection(self):

        # Load database credentials from JSON file
        try:
            with open("credentials.json", "r") as file:
                credentials = json.load(file)
        except FileNotFoundError:
            print(
                "`credentials.json` not found! Make sure you have the credentials from the wiki saved in a JSON file called `credentials.json`"
            )
            print(
                "https://wiki.aris-space.ch/en/rocketry/engines/rotating-detonation"
            )
            sys.exit(1)

        dbConnection = con.connect(
            host=credentials["host"],
            user=credentials["user"],
            password=credentials["password"],
            database=credentials["database"],
        )
        dbCursor = dbConnection.cursor(buffered=True, dictionary=True)
        print("Connection established")
        return dbConnection, dbCursor

    def getTables(self):
        self.cursor.execute("SHOW tables")
        table_rows = self.cursor.fetchall()
        self.tables = pd.DataFrame(table_rows)

    def get_test_date(self, config_id):
        query = f"SELECT date FROM tests WHERE config_id = {config_id}"
        self.cursor.execute(query)
        return self.cursor.fetchone()["date"].strftime("%m-%d-%Y")

    def get_unc(self, sensor, config_id):
        query = f"SELECT unc FROM sensors_meta INNER JOIN sensors ON sensor_id = sensors.id WHERE config_id = {config_id} AND name LIKE '{sensor}'"
        self.cursor.execute(query)
        unc = self.cursor.fetchone()
        return unc["unc"]

    def get_unc_type(self, sensor, config_id):
        query = f"SELECT unc_type FROM sensors_meta INNER JOIN sensors ON sensor_id = sensors.id WHERE config_id = {config_id} AND name LIKE '{sensor}'"
        self.cursor.execute(query)
        unc = self.cursor.fetchone()
        return unc["unc_type"]

    def dfs_from_tables(self, tables):
        dfs = {}
        for table in tables:
            query = f"SELECT * FROM {table}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows)
            dfs[table] = df
        return dfs

    def values_sensors(self, sensors, config_id):
        # Loop over the sensors
        df_list = []
        for sensor in sensors:
            # Create a query to fetch the data
            query = f"SELECT * FROM sensor_values INNER JOIN sensors ON sensor_id = sensors.id WHERE config_id = {config_id} AND name LIKE '{sensor}'"
            # Execute the query and fetch the data
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            # Create a DataFrame from the data
            df_tmp = pd.DataFrame(rows)
            # Add a column with the sensor name
            df_tmp["sensor"] = sensor
            # Append the DataFrame to the list
            df_list.append(df_tmp)
        # Concat the DataFrames into one
        df = pd.concat(df_list, ignore_index=True)
        # Sort the DataFrame by sensor_id and timestamp
        df = df.sort_values(by=["sensor_id", "timestamp"])
        # Drop the columns that are not needed
        df = df.drop(columns=["id", "name", "config_id", "sensor"])
        # Reset the index
        df.reset_index(drop=True, inplace=True)
        return df

    def values_sensors_all(self, sensors):
        values = {}
        for sensor in sensors:
            query = f"SELECT * FROM sensor_values INNER JOIN sensors ON sensor_id = sensors.id WHERE name LIKE '{sensor}'"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows)
            df = df.sort_values(by=["timestamp"])
            values[sensor] = df
        return values
    
    def values_sensors_selected(self, sensors, ids):
        string = "AND ("
        for j, id in enumerate(ids):
            string = string + f"sensors.config_id = {id}"
            if j is not len(ids) - 1:
                string = string + " OR "
        string = string + ")"
        values = {}
        for sensor in sensors:
            query = f"SELECT * FROM sensor_values INNER JOIN sensors ON sensor_id = sensors.id WHERE name LIKE '{sensor}' {string}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows)
            df = df.sort_values(by=["timestamp"])
            values[sensor] = df
        return values

    def values_actuators(self, actuators, config_id):
        # Loop over the actuators
        df_list = []
        for actuator in actuators:
            # Create a query to fetch the data
            query = f"SELECT * FROM actuator_values INNER JOIN actuators ON actuator_id = actuators.id WHERE config_id = {config_id} AND name LIKE '{actuator}'"
            # Execute the query and fetch the data
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            # Create a DataFrame from the data
            df_tmp = pd.DataFrame(rows)
            # Add a column with the actuator name
            df_tmp["actuator"] = actuator
            # Append the DataFrame to the list
            df_list.append(df_tmp)
        # Concat the DataFrames into one
        df = pd.concat(df_list, ignore_index=True)
        # Sort the DataFrame by sensor_id and timestamp
        df = df.sort_values(by=["actuator_id", "timestamp"])
        # Drop the columns that are not needed
        df = df.drop(columns=["id", "name", "config_id", "actuator"])
        # Reset the index
        df.reset_index(drop=True, inplace=True)
        return df
    def values_circuits(self, config_id):
        query = f"SELECT * FROM circuit_values INNER JOIN actuators ON actuator_id = actuators.id WHERE config_id = {config_id}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows)
        return df

    def values_states(self, config_id):
        query = f"SELECT * FROM states WHERE config_id = {config_id}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows)
        return df

    def get_firing_times(self, config_id):
        query = f"SELECT timestamp FROM states WHERE config_id = {config_id} AND state LIKE 'firing confirmation'"
        self.cursor.execute(query)
        firing_start = self.cursor.fetchall()
        firing_starts = []
        for element in firing_start:
            firing_starts.append(element["timestamp"])
        query = f"SELECT timestamp FROM states WHERE config_id = {config_id} AND state LIKE 'POST_FIRING'"
        self.cursor.execute(query)
        firing_end = self.cursor.fetchall()
        firing_ends = []
        for element in firing_end:
            firing_ends.append(element["timestamp"])
        return firing_starts, firing_ends

    def get_actuation_values(self, config_id, actuator_name):
        query = f"SELECT timestamp FROM actuator_values INNER JOIN actuators ON actuator_id = actuators.id WHERE config_id = {config_id} AND value = 1 AND name = '{actuator_name}' ORDER BY timestamp ASC"
        self.cursor.execute(query)
        on = self.cursor.fetchall()
        ons = []
        for element in on:
            ons.append(element["timestamp"])
        query = f"SELECT timestamp FROM actuator_values INNER JOIN actuators ON actuator_id = actuators.id WHERE config_id = {config_id} AND value = 0 AND name = '{actuator_name}' ORDER BY timestamp ASC"
        self.cursor.execute(query)
        off = self.cursor.fetchall()
        offs = []
        for element in off:
            offs.append(element["timestamp"])
        return ons, offs
