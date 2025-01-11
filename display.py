import drivers
import requests
import os
import subprocess
from time import sleep
from datetime import datetime
from gpiozero import CPUTemperature
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

def test_server():
	print("Checking server.")
	hostname = "mylovelyserver.fun"
	command = f'curl -s -o /dev/null -w "%{{http_code}}" {hostname}'
	http_status_code = subprocess.check_output(command, shell=True).decode('utf-8').strip()
	if 200 <= int(http_status_code) <= 300:
		return True
	return False


def set_weather():
	print("Writing weather data.")
	#change url for api calls
	URL = "http://api.weatherapi.com/v1/current.json?key=&q=&aqi=no"
	r = requests.get(url = URL)

	data = r.json()

	temperature = round(data.get("current").get("temp_c"))
	conditions = str(data.get("current").get("condition").get("text")) + " "
	feeling = round(data.get("current").get("feelslike_c"))
	return [temperature, conditions, feeling]

def get_dht_data():
	h, t = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	if h is not None and t is not None:
		return (t, h)
	return (0, 0)


screen = drivers.Lcd()

print("Writing to display")
server_status = 1
weather_data = [0, "Starting... ", 0]
sleep(4)
temperature, humidility = get_dht_data()
time1 = datetime.now()
time2 = datetime.now()
time_temp = datetime.now()
time_change_value = datetime.now()
show_temp = True
first_letter = 0
temptime2 = datetime.now()
temperature = 0
humidility = 0

server_status = test_server()
weather_data = set_weather()

while True:
	line1 = ""

	
	line2 = f"{str(round(weather_data[0])):>2}" + "{0xDF}C "
	
	if datetime.now().timestamp() - time_change_value.timestamp() > 3:
		t, h = get_dht_data()
		if h != 0:
			temperature = t
			humidility = h
		show_temp = not show_temp
		time_change_value = datetime.now()
		print("Temperature: " + str(temperature) + " Humidity: " + str(humidility))

	if show_temp:
		line1 = f"{str(round(temperature)):>2}" + "{0xDF}C "
	else:
		line1 = f"{str(round(float(humidility))):>2}" + "%  "


	if server_status:
		line1 = line1 + str(datetime.fromtimestamp(datetime.now().timestamp()).strftime('%H:%M')) + "  ON"
	else:
		line1 = line1 + str(datetime.fromtimestamp(datetime.now().timestamp()).strftime('%H:%M')) + " !OFF!"
	if datetime.now().timestamp() - temptime2.timestamp() >= 0.4:
		cond_text = ""
		line2 = str(round(weather_data[0]))[:2] + "{0xDF}C "
		for i in range(first_letter, first_letter + 6):
			cond_text = cond_text + weather_data[1][i % (len(weather_data[1]))]

		first_letter = first_letter + 1
		if first_letter >= len(weather_data[1]) - 1:
			first_letter = 0

		line2 = line2 + cond_text + f"{str(round(weather_data[2])):>3}" + "{0xDF}C"
		screen.lcd_display_extended_string(line2, 2)
		temptime2 = datetime.now()
	screen.lcd_display_extended_string(line1, 1)
	if datetime.now().timestamp() - time1.timestamp() >= 600:
		time1 = datetime.now()
		server_status = test_server()
	if datetime.now().timestamp() - time2.timestamp() > 1800:
		time2 = datetime.now()
		weather_data = set_weather()
