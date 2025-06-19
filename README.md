[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/buvnswrn/AJAN-Airsim-Python)
# AJAN-Airsim-Python
A Python API for communicating with Airsim from AJAN Agent System 

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
Else, `WARNING:tornado.general:Connect error on fd 780: WSAECONNREFUSED` will be popping up and the instance quits after some retries or 
If the controller is not executing any actions, it means the Airsimserver has restarted (Typically happens when a new instance of Unity is launched).

## Tech Stack
buvnswrn/AJAN-Airsim-Python is built on the following main stack:

- <img width='25' height='25' src='https://img.stackshare.io/service/1209/javascript.jpeg' alt='JavaScript'/> [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) – Languages
- <img width='25' height='25' src='https://img.stackshare.io/service/2303/New_Project__20_.png' alt='Jinja'/> [Jinja](https://palletsprojects.com/p/jinja/) – Templating Languages & Extensions
- <img width='25' height='25' src='https://img.stackshare.io/service/993/pUBY5pVj.png' alt='Python'/> [Python](https://www.python.org) – Languages
- <img width='25' height='25' src='https://img.stackshare.io/service/989/ruby.png' alt='Ruby'/> [Ruby](https://www.ruby-lang.org) – Languages
- <img width='25' height='25' src='https://img.stackshare.io/service/1001/default_6d109315b60108628b7cd3e159b84645c31ef0e2.png' alt='Flask'/> [Flask](http://flask.pocoo.org/) – Microframeworks (Backend)
- <img width='25' height='25' src='https://img.stackshare.io/service/2993/2DZC4KaA_400x400.jpg' alt='Matplotlib'/> [Matplotlib](http://matplotlib.org) – Charting Libraries
- <img width='25' height='25' src='https://img.stackshare.io/service/1002/tornado.png' alt='Tornado'/> [Tornado](http://www.tornadoweb.org/) – Frameworks (Full Stack)
- <img width='25' height='25' src='https://img.stackshare.io/service/3670/mqtticon-large_400x400.png' alt='MQTT'/> [MQTT](http://mqtt.org/) – Message Queue
- <img width='25' height='25' src='https://img.stackshare.io/service/5559/-RIWgodF_400x400.jpg' alt='pip'/> [pip](https://pypi.org/project/pip/) – Front End Package Manager
- <img width='25' height='25' src='https://img.stackshare.io/service/1293/opencv-logo-64x64.png' alt='OpenCV'/> [OpenCV](http://opencv.org/) – Image Processing and Management
- <img width='25' height='25' src='https://img.stackshare.io/service/2375/default_1f67b0ca7416a9f52beb655f90b5602d5ef74b75.jpg' alt='Pillow'/> [Pillow](https://python-pillow.github.io/) – Image Processing and Management
- <img width='25' height='25' src='https://img.stackshare.io/service/2179/default_332f874a2edb2686f578aa6389313efcea1eec41.png' alt='NumPy'/> [NumPy](http://www.numpy.org/) – Data Science Tools
- <img width='25' height='25' src='https://img.stackshare.io/service/2180/1284191.png' alt='Pandas'/> [Pandas](http://pandas.pydata.org/) – Data Science Tools
- <img width='25' height='25' src='https://img.stackshare.io/service/3303/scipyshiny_small.png' alt='SciPy'/> [SciPy](http://www.scipy.org) – Data Science Tools

Full tech stack [here](/techstack.md)
