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
> **Explanation:**
> **RabbitMQ Integration:** The script now includes a function publish_data_to_rabbitmq that connects to RabbitMQ and publishes the formatted pressure data as a message to the specified queue (RABBITMQ_QUEUE).
> **Data Formatting: **The data is formatted into a string containing index, epoch time, current time, and pressure value.
> **Connection Parameters:** Replace RABBITMQ_HOST with your RabbitMQ server's hostname or IP address.
> Ensure your RabbitMQ server is running and accessible from the machine where this script will run.
> Modify RABBITMQ_QUEUE if needed to match the queue name you want to use in RabbitMQ.
