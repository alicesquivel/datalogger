> [!CAUTION]
> This is a work in progress.

# Waveshare SenseHAT with Raspbery PI 
https://www.waveshare.com/wiki/Sense_HAT_(B)


<img width="1176" alt="image" src="https://github.com/user-attachments/assets/facf42fb-b988-4493-a587-7f76d80f611d">


# datalogger
Data aggregator setup  

## Mosquitto 
Here are the steps and installations you need to set up your Raspberry Pi to run the script using Mosquitto:

**Update and Upgrade Your Raspberry Pi** 

First, make sure your Raspberry Pi is up to date: 
```
sudo apt-get update
sudo apt-get upgrade
```

**Install Python and Required Libraries** 

Ensure you have Python and the required libraries installed:
```
sudo apt-get install python3 python3-pip
pip3 install smbus2 paho-mqtt
```

**Install and Configure Mosquitto (MQTT Broker)**

Install Mosquitto:
```
sudo apt-get install mosquitto mosquitto-clients
```
**Enable Mosquitto to start on boot:**
```
sudo systemctl enable mosquitto
```
**Start the Mosquitto service:**
```
sudo systemctl start mosquitto
```

**Configure Mosquitto (Optional)**

You can configure Mosquitto if you need specific settings or authentication. By default, Mosquitto will run with basic configurations suitable for most local setups.

**Run the Python Script**

Now you can run your Python script:
```
python3 sensor_data_collector_mosquitto.py
```

**Additional Steps for Testing and Debugging**

You can use Mosquitto clients to publish and subscribe to topics for testing:
```
mosquitto_pub -h localhost -t 'test/topic' -m 'Hello, MQTT'
mosquitto_sub -h localhost -t 'test/topic'
```
**Monitor the MQTT messages being published by your script:**
```
mosquitto_sub -h 172.16.7.97 -t 'pressure_data'
```

> [!CAUTION]
> The error ConnectionRefusedError: [Errno 111] Connection refused suggests that the script is unable to connect to the MQTT broker at 172.16.7.97. This could be due to several reasons such as the broker not running, network issues, or incorrect configuration.

**Here's a step-by-step guide to troubleshoot and resolve this issue:**

**Step 1: Ensure Mosquitto is Running**

Check if the Mosquitto broker is running on your Raspberry Pi:
```
sudo systemctl status mosquitto
```

If it is not running, start the service:
```
sudo systemctl start mosquitto
```
**Step 2: Verify the Broker Configuration**

Ensure that the Mosquitto broker is configured correctly. You can check the configuration file located at /etc/mosquitto/mosquitto.conf. By default, Mosquitto listens on port 1883.

**Step 3: Test the MQTT Broker Locally**

Run a simple test to ensure the MQTT broker is working locally:
Open a terminal and run the subscriber:
```
mosquitto_sub -h localhost -t 'test/topic'
```
**Open another terminal and publish a message:**
```
mosquitto_pub -h localhost -t 'test/topic' -m 'Hello, MQTT'
```
If you see the message in the subscriber terminal, the broker is working locally.

**Step 4: Check Network Connectivity**

Ensure that your device running the script can reach the MQTT broker at 172.16.7.97. You can use the ping command to check connectivity:
```
ping 172.16.7.97
```
If the broker is running on the same Raspberry Pi, you can use localhost or 127.0.0.1 as the MQTT_BROKER.

**Step 5: Update the Script (if needed)**

If the broker is running locally, update the script to use localhost as the broker address:
```
MQTT_BROKER = 'localhost'
```
**Step 6: Run the Script Again** 

Try running the script again:
```
python3 mosquitto.py
```

# InfluxDB and Telegraf in Chameleon node

## Installing InfluxDB on Ubuntu 22.04 (x86_64)
You can also follow the documentation from the InfluxDB website. [Install InfluxDB](https://docs.influxdata.com/influxdb/v2/install/#download-and-install-influxdb-v2) 
