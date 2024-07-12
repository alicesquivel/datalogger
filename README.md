> [!CAUTION]
> This is a work in progress.

# datalogger
Data aggregator setup for Avis deployments  

## Mosquitto
Here are the steps and installations you need to set up your Raspberry Pi to run the script using Mosquitto:

### Step 1: Update and Upgrade Your Raspberry Pi
First, make sure your Raspberry Pi is up to date:
```
sudo apt-get update
sudo apt-get upgrade
```

### Step 2: Install Python and Required Libraries
Ensure you have Python and the required libraries installed:
```
sudo apt-get install python3 python3-pip
pip3 install smbus2 paho-mqtt
```

### Step 3: Install and Configure Mosquitto (MQTT Broker)
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

### Step 4: Configure Mosquitto (Optional)
You can configure Mosquitto if you need specific settings or authentication. By default, Mosquitto will run with basic configurations suitable for most local setups.

### Step 5: Run the Python Script
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
Open another terminal and publish a message:
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

### To send data from your MQTT broker to Telegraf and then save it to InfluxDB, you'll need to follow these steps:
1. Install and Configure Telegraf
2. Configure Telegraf to Subscribe to MQTT Topics
3. Configure Telegraf to Write to InfluxDB

**Step 1: Install Telegraf**
If you haven't already installed Telegraf, you can do so with the following commands:
```
sudo apt-get update
sudo apt-get install telegraf
```
**Step 2: Configure Telegraf to Subscribe to MQTT Topics**
Edit the Telegraf Configuration File:
Open the Telegraf configuration file:
```
sudo nano /etc/telegraf/telegraf.conf
```

Add MQTT Consumer Plugin:
Add the following configuration for the MQTT consumer plugin. This configuration tells Telegraf to subscribe to the pressure_data topic on your MQTT broker:
```
[[inputs.mqtt_consumer]]
  servers = ["tcp://localhost:1883"]
  topics = ["pressure_data"]
  qos = 0
  connection_timeout = "30s"
  client_id = ""
  username = ""
  password = ""
  data_format = "influx"

  [[inputs.mqtt_consumer.tags]]
    influxdb_database = "sensor"  # Name of the InfluxDB database
    influxdb_retention_policy = ""  # Retention policy, if any
```
**Step 3: Configure Telegraf to Write to InfluxDB**
Add InfluxDB Output Plugin:
In the same telegraf.conf file, add the configuration for the InfluxDB output plugin. This configuration tells Telegraf to send the collected data to your InfluxDB instance:
```
[[outputs.influxdb_v2]]
  urls = ["http://localhost:8086"]
  token = "GRE_ALDeZdPSkz867xMDtQWQP2w9UNRUUtYo7GxH_p6mmXbNrT3fjuIMsYGFGYFPCijGeGAdgK_JnnrCCZG1oA=="
  organization = "uchicago"
  bucket = "sensor"
```
**Step 4: Start and Enable Telegraf**
Enable Telegraf to start on boot and then start the service:
```
sudo systemctl enable telegraf
sudo systemctl start telegraf
```
**Step 5: Verify the Setup**
Check Telegraf Logs:
Ensure that Telegraf is running without errors:
```
sudo journalctl -u telegraf -f
```
Verify Data in InfluxDB:
Check your InfluxDB instance to verify that data is being written. You can use the InfluxDB UI or CLI to query the data.

# Telegraf in a Chameleon node

**Step 1: Install Telegraf on the Cloud Node**
Follow the instructions to set up a virtual machine (VM) or server in Chameleon, and then install Telegraf on that machine. For Ubuntu, you can use the following commands:
```
sudo apt-get update
sudo apt-get install -y telegraf
```
**Step 2: Configure Telegraf to Subscribe to MQTT Topics**
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

**Step 3: Configure InfluxDB**
Ensure InfluxDB is running and properly configured on the same cloud node or another node. You can follow the official InfluxDB installation instructions for your cloud environment. Make sure you have created a bucket and an API token.

**Step 4: Start Telegraf**
Start and enable Telegraf on the cloud node:
```
sudo systemctl start telegraf
sudo systemctl enable telegraf
```
**Step 5: Test the Setup**
Publish data to the MQTT broker on your Raspberry Pi using your Python script.
Verify Telegraf is receiving data from the MQTT broker. Check the Telegraf logs on the cloud node:
```
sudo journalctl -u telegraf -f
```
Verify data in InfluxDB by querying the InfluxDB instance or using a tool like Chronograf or Grafana to visualize the data.
Example of Python Script Publishing Data to MQTT
Your Python script should remain unchanged as it is already configured to publish data to the MQTT broker.

> [!Troubleshooting]
> **1. Network Issues:** Ensure that there are no network issues preventing the cloud node from reaching the MQTT broker on your Raspberry Pi. <br>
> **2. Firewall Rules:** Make sure that any firewalls or security groups allow traffic on the necessary ports (1883 for MQTT and 8086 for InfluxDB). <br>
> **3. Logs:** Check the logs of Telegraf and InfluxDB for any error messages that could help in diagnosing issues. <br>
This setup should allow you to send sensor data from your Raspberry Pi to an MQTT broker, then have Telegraf on a cloud node subscribe to the MQTT topics, and finally write the data to InfluxDB.

# RabbitMQ

# setup
To integrate data collection with RabbitMQ, you'll need to install the pika library, which provides a Python interface for RabbitMQ. 
Here’s how you can modify your script to publish the pressure data to RabbitMQ:

## Install pika Library:
Ensure you have pika installed. You can install it using pip if you haven't already:
```
pip install pika
```
## Modify the Script:
Modify the existing script to publish the pressure data to RabbitMQ:
```
sensor_data_collector.py
```

> [!Note]
> **RabbitMQ Integration:** The script now includes a function publish_data_to_rabbitmq that connects to RabbitMQ and publishes the formatted pressure data as a message to the specified queue (RABBITMQ_QUEUE).

> **Data Formatting:** The data is formatted into a string containing index, epoch time, current time, and pressure value.

> **Connection Parameters:** Replace RABBITMQ_HOST with your RabbitMQ server's hostname or IP address.
> Ensure your RabbitMQ server is running and accessible from the machine where this script will run.
> Modify RABBITMQ_QUEUE if needed to match the queue name you want to use in RabbitMQ.

## Installing RabbitMQ on Raspberry Pi
If you haven't installed RabbitMQ yet, you can do so using the following commands:
```
sudo apt update
sudo apt install rabbitmq-server
```
**Configuring RabbitMQ**
Enable RabbitMQ Management Plugin:
Enable the RabbitMQ Management Plugin to access the web management interface:
```
sudo rabbitmq-plugins enable rabbitmq_management
```
**Accessing RabbitMQ Management Interface:**
Once enabled, you can access the RabbitMQ management interface from a web browser:
Open a web browser on any computer within the same network as your Raspberry Pi.
Navigate to http://172.16.7.97:15672 (replace 172.16.7.97 with the actual IP address of your Raspberry Pi where RabbitMQ is installed).
Log in with the default credentials:
```
Username: guest
Password: guest
```
> [!Note]
> For production use, it's recommended to change the default credentials and set up secure access.
**Creating a Queue:**
From the RabbitMQ management interface, go to the Queues tab.
Click on Add a new queue.
Enter a name for your queue (e.g., pressure_data).
Leave other settings as default or configure them as per your requirements.
Click Add queue to create the queue.
**Setting Up Permissions:**
It’s important to set up permissions so that your Python script can publish messages to the queue:
* Go to the Admin tab and click on Add a user.
* Enter a username and password for your new user (e.g., producer with password producer123).
* Click Add user to create the user.
* After creating the user, click on the Set permissions button next to the user.
* Choose your newly created queue (pressure_data) from the dropdown list.
* Grant the user permissions to configure, write, and read operations on the queue.
* Click Set permissions to apply.
  
## Note Down RabbitMQ Connection Details:
**Before running your Python script, note down the following RabbitMQ connection details:**
```
Host: IP address of your Raspberry Pi (172.16.7.97 in your case).
Port: RabbitMQ default port is 5672.
Virtual Host: Default virtual host is /.
Username and Password: Credentials of the user you created (e.g., producer / producer123).
```

**Running the Script**
* Save the updated script on your Raspberry Pi.
* Open a terminal and navigate to the directory containing your script.

Run the script using Python:
```
python3 pressure_sensor_script.py
```
Monitor the terminal for messages indicating that data is being published to RabbitMQ.

**Verifying RabbitMQ Setup**
* Access the RabbitMQ management interface (http://172.16.7.97:15672) from your web browser.
* Navigate to the Queues tab and verify that the pressure_data queue shows messages being delivered.

# Connecting RabbitMQ to Telegraf
To connect your script to Telegraf for integration with InfluxDB, you need to update your script to publish data in a format that Telegraf can read from a RabbitMQ queue. Telegraf will then forward this data to InfluxDB.

**Step 1:** Update the Python Script
Modify the script to remove direct InfluxDB writes and ensure it publishes data to RabbitMQ in a format that Telegraf can parse.

**Step 2:** Configure Telegraf
Install Telegraf (if not already installed):
```
sudo apt-get update
sudo apt-get install telegraf
Configure Telegraf to read from RabbitMQ and write to InfluxDB:
```

Edit the Telegraf configuration file (usually located at /etc/telegraf/telegraf.conf):
```
sudo nano /etc/telegraf/telegraf.conf
Add the RabbitMQ input and InfluxDB output plugins:
```

```
[[inputs.rabbitmq]]
  url = "amqp://producer:producer123@172.16.7.97:5672"
  # Assuming pressure_data queue
  queue_name_include = ["pressure_data"]
  data_format = "influx"

[[outputs.influxdb_v2]]
  urls = ["http://172.16.7.97:8086"]
  token = "ZqvyCLLID504lvrHgS0GMx8M_bG4cicy5zZEuk4MKbNo3rkek9xyDfK6iJqwcp6BjPPkyijMb4zFSFDoEQFVQg=="
  organization = "uchicago"
  bucket = "sensor"
```

Restart Telegraf to apply the configuration changes:
```
sudo systemctl restart telegraf
```

**Step 3:** Verify the Setup
Run your Python script:
```
python your_script_name.py
```

Check Telegraf logs to ensure data is being processed:
```
sudo journalctl -u telegraf -f
```
Verify data in InfluxDB:
You can use the InfluxDB UI or influx CLI to query the data.




