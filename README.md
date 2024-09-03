# Raspberry OLED + FanControl (OS: Bookworm)

### Before enything we need to create a virtual environment
To create a virtual environment on a Raspberry Pi 4/5, you'll typically be using Python's built-in venv module. Here's how you can do it step-by-step:

### 1. Update Your System:
First, ensure that your Raspberry Pi's package lists are up to date.
```
sudo apt-get update
sudo apt-get upgrade -y
```
### 2. Install Python (if not already installed):
Raspberry Pi OS usually comes with Python pre-installed. You can check if Python is installed by running:
```
python3 --version
```
If Python isn't installed, you can install it using:
```
sudo apt-get install python3
```
### 3. Install 'venv' (if not already installed):
The **_'venv'_** module should come with Python by default, but if it’s not installed, you can install it with:
```
sudo apt-get install python3-venv
```
### 4. Create a Virtual Environment:
Navigate to the directory where you want to create your virtual environment or create a new directory:
```
mkdir 'myproject'
cd 'myproject'
```
Now, create a virtual environment using the following command:
```
python3 -m venv 'myenv'
```
Here, **_'myenv'_** is the name of the virtual environment folder. You can name it whatever you like.

### 5. Activate the Virtual Environment:
To activate the virtual environment, use the following command:
```
source 'myenv'/bin/activate
```
Once activated, your command prompt will change to show that you are now operating within the virtual environment.

### 6. Install Packages:
```
*sudo pip3 install --upgrade adafruit-python-shell --break-system-packages
```
Requirement already satisfied
```
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
```
```
sudo python3 raspi-blinka.py
```
```
* sudo pip3 install adafruit-circuitpython-ssd1306 --break-system-packages
```
Some requirement already satisfied
```
* sudo pip3 install psutil --break-system-packages
```
Requirement already satisfied, already the newest version
```
* sudo apt-get install python3-pil
```
Already the newest version

### 7. DOWNLOAD and COPY script and font
```
git clone https://github.com/shoro/RPi_OLED_FanControl.git
```
# Autorun on raspberry startup
### Create a Script to activate the Virtual Environment
First, you need a script that will activate the virtual environment and run your application.

1. Create a script (e.g., start_app.sh):
```
sudo nano ~/start_app.sh
```
2. Add the following lines to the script:
```
#!/bin/bash
cd /path/to/your/project
source /path/to/your/venv/env/bin/activate
python your_script.py
```
Replace /path/to/your/project with the directory where your project resides.

Replace /path/to/your/venv with the path to your virtual environment.

Replace your_script.py with the name of the Python script you want to run.

3. Make the script executable:
```
sudo chmod +x ~/start_app.sh
```
4. Use crontab to Run the Script at Boot
```
sudo crontab -e
```
5. Add a new line at the end of the file:
```
@reboot /path/to/your/app/start_app.sh
```

OPTIONAL
Log Output: If you want to capture the output of your script, you can modify the crontab entry like this:
```
@reboot /path/to/your/app/start_app.sh >> /path/to/your/log/app_log.txt 2>&1
```
