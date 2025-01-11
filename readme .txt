Weather, indoor temperature and humidity, clock and server status checker display for raspberry pi with lcd I2C display.

How to install?
enable I2C in raspberry pi
sudo apt install git
cd /home/${USER}/
git clone https://github.com/the-raspberry-pi-guy/lcd.git
cd lcd/
sudo ./install.sh
paste display.py in lcd folder
and service file service to /lib/systemd/system
sudo apt install python3-pip
pip install Adafruit_DHT --break-system-packages