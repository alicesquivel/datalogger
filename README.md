> [!CAUTION]
> This is a work in progress.

# datalogger
Data aggregator setup for Avis deployments  

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

## Install InfluxDB
First, you'll need to install and configure InfluxDB:

**Installation:** Follow the official InfluxDB installation instructions for your operating system.

**Configuration:** Configure InfluxDB, including creating databases and setting up authentication if necessary. You typically interact with InfluxDB through its command-line interface (CLI) or API.

## Install Telegraf
Telegraf is used to collect, process, and send metrics to InfluxDB. You can install it on the same machine where your Python script runs or on a separate server if needed:

**Installation:** Follow the Telegraf installation instructions for your platform.

**Configuration:** Configure Telegraf to collect data from RabbitMQ. You'll need to edit Telegraf's configuration file (telegraf.conf) to include an input plugin for RabbitMQ and an output plugin for InfluxDB. Here’s a basic example:

```
[[inputs.rabbitmq_consumer]]
  name = "rabbitmq_consumer"
  endpoints = ["amqp://guest:guest@localhost:5672/"]  # Adjust RabbitMQ connection details
  queue = "pressure_data"  # Adjust to match your RabbitMQ queue name
  consumer_tag = "telegraf"
  data_format = "json"

[[outputs.influxdb_v2]]
  urls = ["http://localhost:8086"]  # Adjust InfluxDB URL if necessary
  token = "$INFLUXDB_TOKEN"
  organization = "your_organization"
  bucket = "your_bucket"
```

**Replace guest:** guest@localhost:5672/ with your RabbitMQ connection details and adjust other parameters as needed.

## Installing RabbitMQ on Raspberry Pi
If you haven't installed RabbitMQ yet, you can do so using the following commands:

bash
Copy code
```
sudo apt update
sudo apt install rabbitmq-server
```

**Configuring RabbitMQ**
Enable RabbitMQ Management Plugin:
Enable the RabbitMQ Management Plugin to access the web management interface:

bash
Copy code
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

Go to the Admin tab and click on Add a user.
Enter a username and password for your new user (e.g., producer with password producer123).
Click Add user to create the user.
After creating the user, click on the Set permissions button next to the user.
Choose your newly created queue (pressure_data) from the dropdown list.
Grant the user permissions to configure, write, and read operations on the queue.
Click Set permissions to apply.
Note Down RabbitMQ Connection Details:

**Before running your Python script, note down the following RabbitMQ connection details:**

Host: IP address of your Raspberry Pi (172.16.7.97 in your case).
Port: RabbitMQ default port is 5672.
Virtual Host: Default virtual host is /.
Username and Password: Credentials of the user you created (e.g., producer / producer123).

