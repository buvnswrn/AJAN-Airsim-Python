# AJAN-Airsim-Python
A Python API for communicating with Airsim

## Installation
- Create a virtual environment using the following command
```python -m venv AJAN-Airsim-Python```
- Install the requirements.txt file using pip
```pip install -r requirements.txt```

## Usage
- activate the virtual environment. Goto the directory where the virtual environment is created and run the following command
```AJAN-Airsim-Python\Scripts\activate``` or go to the directory ```AJAN-Airsim-Python\Scripts``` and run the command ```activate```
- 
```python app.py```
To start the application, run the app.py file. By default, the application will start and connect to the Airsim simulator.
- access the application by going to the following URL in a web browser
```http://localhost:5002```
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

## Ports
- The application runs on port `5002` by default.

Note: Only one of the enableAirsim and enableRealWorldExecution can be set to True at a time, if both resources are not available.
Note: Airsim should be running before the application is started. and should always be restarted when the simulation is restarted.

