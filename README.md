> [!CAUTION]
> This is a work in progress.

# Waveshare SenseHAT with Raspbery PI 
https://www.waveshare.com/wiki/Sense_HAT_(B)


<img width="1176" alt="image" src="https://github.com/user-attachments/assets/facf42fb-b988-4493-a587-7f76d80f611d">


# datalogger
Data aggregator setup  

## Mosquitto 
Here are the steps and installations you need to set up your Raspberry Pi to run the script using Mosquitto:

**Step 1: Update and Upgrade Your Raspberry Pi** 

First, make sure your Raspberry Pi is up to date: 
```
sudo apt-get update
sudo apt-get upgrade
```

**Step 2: Install Python and Required Libraries** 

Ensure you have Python and the required libraries installed:
```
sudo apt-get install python3 python3-pip
pip3 install smbus2 paho-mqtt
```

**Step 3: Install and Configure Mosquitto (MQTT Broker)**

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

**Step 4: Configure Mosquitto (Optional)**

You can configure Mosquitto if you need specific settings or authentication. By default, Mosquitto will run with basic configurations suitable for most local setups.

**Step 5: Run the Python Script**

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
Add InfluxData repository:
```
wget -qO- https://repos.influxdata.com/influxdb.key | sudo gpg --dearmor -o /usr/share/keyrings/influxdb-archive-keyring.gpg
```
Set up the stable repository:

```
echo "deb [signed-by=/usr/share/keyrings/influxdb-archive-keyring.gpg] https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
```

Update the package list:
```
sudo apt-get update
```

Install InfluxDB:
```
sudo apt-get install influxdb
```

Start and enable the InfluxDB service:
```
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb
```

Verify InfluxDB status (optional):
```
sudo systemctl status influxdb
```

Access the InfluxDB CLI:
```
influx
```

Install InfluxDB CLI:
```
sudo apt install influxdb-client
```

Create a database and user for Telegraf
Inside the InfluxDB CLI, execute the following commands:
```
CREATE DATABASE your_database_name
CREATE USER your_username WITH PASSWORD 'your_password'
GRANT ALL ON your_database_name TO your_username
```

Replace your_database_name, your_username, and 'your_password' with your desired database name, username, and password.

**Exit the InfluxDB CLI:**
```
EXIT
```
> [!CAUTION]
> **Additional Notes**
> InfluxDB should now be installed and running on your system. You can access the InfluxDB web interface at http://localhost:8086 to manage and visualize your data.
> Configure your Telegraf instance to send data to InfluxDB using the credentials (your_database_name, your_username, your_password) you set up.

**Step 2: Install Telegraf on Ubuntu 22.04 (x86_64)
Follow the instructions to set up a virtual machine (VM) or server in Chameleon, and then install Telegraf on that machine. For Ubuntu, you can use the following commands:
```
sudo apt-get update
sudo apt-get install -y telegraf
```
## Configure Telegraf to Subscribe to MQTT Topics** <br>
Edit the Telegraf configuration file to include the MQTT input plugin. You can typically find the Telegraf configuration file at /etc/telegraf/telegraf.conf. Add the following configuration to this file:
```
[[inputs.mqtt_consumer]]
  servers = ["tcp://YOUR_RASPBERRY_PI_IP:1883"]
  topics = ["pressure_data"]
  qos = 0
  connection_timeout = "30s"
  persistent_session = true
  client_id = "telegraf"
  username = ""
  password = ""
  data_format = "influx"

[[outputs.influxdb]]
  urls = ["http://localhost:8086"] # URL of your InfluxDB instance
  token = "YOUR_INFLUXDB_API_TOKEN"
  organization = "uchicago"
  bucket = "sensor"
```
Replace YOUR_RASPBERRY_PI_IP with the IP address of your Raspberry Pi, and YOUR_INFLUXDB_API_TOKEN with your actual InfluxDB API token.

### Configure InfluxDB** <br>
Ensure InfluxDB is running and properly configured on the same cloud node or another node. You can follow the official InfluxDB installation instructions for your cloud environment. Make sure you have created a bucket and an API token.

### Start Telegraf** <br>
Start and enable Telegraf on the cloud node:
```
sudo systemctl start telegraf
sudo systemctl enable telegraf
```
### Test the Setup** <br>
Publish data to the MQTT broker on your Raspberry Pi using your Python script.
Verify Telegraf is receiving data from the MQTT broker. Check the Telegraf logs on the cloud node:
```
sudo journalctl -u telegraf -f
```
Verify data in InfluxDB by querying the InfluxDB instance or using a tool like Chronograf or Grafana to visualize the data.
Example of Python Script Publishing Data to MQTT
Your Python script should remain unchanged as it is already configured to publish data to the MQTT broker.

> [!CAUTION]
> **1. Network Issues:** Ensure that there are no network issues preventing the cloud node from reaching the MQTT broker on your Raspberry Pi. <br>
> **2. Firewall Rules:** Make sure that any firewalls or security groups allow traffic on the necessary ports (1883 for MQTT and 8086 for InfluxDB). <br>
> **3. Logs:** Check the logs of Telegraf and InfluxDB for any error messages that could help in diagnosing issues. <br>
This setup should allow you to send sensor data from your Raspberry Pi to an MQTT broker, then have Telegraf on a cloud node subscribe to the MQTT topics, and finally write the data to InfluxDB.

