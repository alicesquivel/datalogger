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

