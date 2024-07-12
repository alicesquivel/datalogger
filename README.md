> [!CAUTION]
> This is a work in progress.

# datalogger
Data aggregator setup for Avis deployments  

## options
Mosquitto and RabbitMQ

## Mosquitto

## RabbitMQ

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




