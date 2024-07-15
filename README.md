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
# Download the InfluxDB package for AMD64
```
curl -LO https://download.influxdata.com/influxdb/releases/influxdb2_2.7.7-1_amd64.deb
```
# Install the package
```
sudo dpkg -i influxdb2_2.7.7-1_amd64.deb
```
Start the InfluxDB service:
```
sudo service influxdb start
```
Installing the InfluxDB package creates a service file at /lib/systemd/system/influxdb.service to start InfluxDB as a background service on startup.

To verify that the service is running correctly, restart your system and then enter the following command in your terminal:
```
sudo service influxdb status
```
If successful, the output is the following:

<img width="895" alt="image" src="https://github.com/user-attachments/assets/2fa25e8d-5ef9-45dc-bdb2-967b190c2acf">

### Pass configuration options to the service

You can use systemd to customize InfluxDB [configuration options](https://docs.influxdata.com/influxdb/v2/reference/config-options/#configuration-options) and pass them to the InfluxDB service.

Edit the ```/etc/default/influxdb2 ``` service configuration file to assign configuration directives to influxd command line flags–for example, add one or more <ENV_VARIABLE_NAME>=<COMMAND_LINE_FLAG> lines like the following:
```
ARG1="--http-bind-address :8087"
ARG2="--storage-wal-fsync-delay=15m"
```
Edit the /lib/systemd/system/influxdb.service file to pass the variables to the ExecStart value:
```
ExecStart=/usr/bin/influxd $ARG1 $ARG2
```
## Step-by-Step Instructions:
Edit the ```/etc/default/influxdb2``` File:

This file allows you to set environment variables that the InfluxDB service will use. You should add your custom configuration directives here.
```
sudo nano /etc/default/influxdb2
```
Add the configuration directives by defining the environment variables. For example:
```
ARG1="--http-bind-address=:8087"
ARG2="--storage-wal-fsync-delay=15m"
```
Save and close the file (Ctrl+O, Enter, Ctrl+X).

Ensure the Systemd Service File References the Environment File:
The provided service file already includes the EnvironmentFile directive. Make sure it is correct and doesn't need any further modification. Here is the relevant section:
```
[Service]
User=influxdb
Group=influxdb
LimitNOFILE=65536
EnvironmentFile=-/etc/default/influxdb2
ExecStart=/usr/lib/influxdb/scripts/influxd-systemd-start.sh
KillMode=control-group
Restart=on-failure
Type=forking
PIDFile=/var/lib/influxdb/influxd.pid
StateDirectory=influxdb
StateDirectoryMode=0750
LogsDirectory=influxdb
LogsDirectoryMode=0750
UMask=0027
TimeoutStartSec=0
```
Modify the ExecStart Script:

The ExecStart directive in the systemd service file calls a script ```(/usr/lib/influxdb/scripts/influxd-systemd-start.sh)```. This script should be modified to include the environment variables.
Open the script:
```
sudo nano /usr/lib/influxdb/scripts/influxd-systemd-start.sh
```
Modify the script to use the environment variables defined in /etc/default/influxdb2. For example:
```
#!/bin/bash
exec /usr/bin/influxd $ARG1 $ARG2
```
Save and close the script (Ctrl+O, Enter, Ctrl+X).

Reload Systemd and Restart the Service:

After editing the configuration files, reload the systemd configuration and restart the InfluxDB service to apply the changes.
```
sudo systemctl daemon-reload
sudo systemctl restart influxdb
```
Verify the Service Status:
Ensure that the InfluxDB service is running with the new configuration.
```
sudo systemctl status influxdb
```
