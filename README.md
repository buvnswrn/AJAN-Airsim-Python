# AJAN-Airsim-Python
A Python API for communicating with Airsim

## Installation
Install the requirements.txt file using pip
```pip install -r requirements.txt```

## Usage
```python app.py```
To start the application, run the app.py file. By default, the application will start and connect to the Airsim simulator.

## Configuration
- The config.ini file contains the configuration for the Airsim simulator. The IP address and port number can be changed to match the configuration of the Airsim simulator.
Modify the config.ini file to change the configuration of the Airsim simulator or execute in real world and not simulation.

    ```
    [DEFAULT]
    enableAirsim = True # Set to False to disable Airsim
    enableRealWorldExecution = False # Set to True to enable real world execution
    
    [AIRSIM]
    ip = 192.168.178.154 # IP address of the Airsim simulator
    port = 41451 # Port number of the Airsim simulator
    ```
- Normally the PyCharm IDE is used to run which uses the config- Env variable: `PYTHONUNBUFFERED=1`

Note: Only one of the enableAirsim and enableRealWorldExecution can be set to True at a time, if both resources are not available.
Note: Airsim should be running before the application is started.

