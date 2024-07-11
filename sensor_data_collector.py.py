#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from datetime import datetime
import smbus
import pika  # Import RabbitMQ library
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB configuration
INFLUXDB_URL = "http://172.16.7.97:8086"
INFLUXDB_TOKEN = "ZqvyCLLID504lvrHgS0GMx8M_bG4cicy5zZEuk4MKbNo3rkek9xyDfK6iJqwcp6BjPPkyijMb4zFSFDoEQFVQg=="
INFLUXDB_ORG = "uchicago"
INFLUXDB_BUCKET = "sensor"

# RabbitMQ configuration
RABBITMQ_HOST = '172.16.7.97'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'producer'
RABBITMQ_PASSWORD = 'producer123'
RABBITMQ_QUEUE = 'pressure_data'

# I2C address
LPS22HB_I2C_ADDRESS = 0x5C

# Register addresses
LPS_ID = 0xB1
LPS_WHO_AM_I = 0x0F
LPS_CTRL_REG1 = 0x10
LPS_CTRL_REG2 = 0x11
LPS_STATUS = 0x27
LPS_PRESS_OUT_XL = 0x28
LPS_PRESS_OUT_L = 0x29
LPS_PRESS_OUT_H = 0x2A

class LPS22HB(object):
    def __init__(self, address=LPS22HB_I2C_ADDRESS):
        self._address = address
        self._bus = smbus.SMBus(1)
        self.LPS22HB_RESET()
        self._write_byte(LPS_CTRL_REG1, 0x02)

    def LPS22HB_RESET(self):
        Buf = self._read_u16(LPS_CTRL_REG2)
        Buf |= 0x04
        self._write_byte(LPS_CTRL_REG2, Buf)
        while Buf:
            Buf = self._read_u16(LPS_CTRL_REG2)
            Buf &= 0x04

    def LPS22HB_START_ONESHOT(self):
        Buf = self._read_u16(LPS_CTRL_REG2)
        Buf |= 0x01
        self._write_byte(LPS_CTRL_REG2, Buf)

    def _read_byte(self, cmd):
        return self._bus.read_byte_data(self._address, cmd)

    def _read_u16(self, cmd):
        LSB = self._bus.read_byte_data(self._address, cmd)
        MSB = self._bus.read_byte_data(self._address, cmd + 1)
        return (MSB << 8) + LSB

    def _write_byte(self, cmd, val):
        self._bus.write_byte_data(self._address, cmd, val)

def publish_data_to_rabbitmq(data):
    # Connect to RabbitMQ server
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)  # Ensure queue exists and is durable

    # Publish data to RabbitMQ queue
    channel.basic_publish(exchange='',
                          routing_key=RABBITMQ_QUEUE,
                          body=data,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # Make message persistent
                          ))
    print(f" [x] Sent {data} to RabbitMQ")
    connection.close()

def write_to_influxdb(index, epoch_time, pressure_data):
    # Create a connection to InfluxDB
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Define the point to write
    point = Point("pressure") \
        .tag("index", index) \
        .field("epoch_time", epoch_time) \
        .field("pressure", pressure_data)

    # Write point to InfluxDB
    write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)

    # Close client connection
    client.close()

if __name__ == '__main__':
    PRESS_DATA = 0.0
    u8Buf = [0, 0, 0]
    print("\nPressure Sensor Test Program ...\n")
    lps22hb = LPS22HB()

    index = 0

    while True:
        try:
            time.sleep(0.1)
            lps22hb.LPS22HB_START_ONESHOT()
            if (lps22hb._read_byte(LPS_STATUS) & 0x01) == 0x01:  # a new pressure data is generated
                u8Buf[0] = lps22hb._read_byte(LPS_PRESS_OUT_XL)
                u8Buf[1] = lps22hb._read_byte(LPS_PRESS_OUT_L)
                u8Buf[2] = lps22hb._read_byte(LPS_PRESS_OUT_H)
                PRESS_DATA = ((u8Buf[2] << 16) + (u8Buf[1] << 8) + u8Buf[0]) / 4096.0

                # Get current epoch time and formatted time
                epoch_time = int(time.time())
                epoch_str = str(epoch_time)
                current_time = datetime.now().strftime("%S/%d/%m/%Y")

                # Prepare data to publish
                data = f'Index: {index}, Epoch Time: {epoch_str}s, Time: {current_time}, Pressure: {PRESS_DATA:.2f} hPa'

                # Print data for reference
                print(data)

                # Publish data to RabbitMQ
                publish_data_to_rabbitmq(data)

                # Write data to InfluxDB
                write_to_influxdb(index, epoch_time, PRESS_DATA)

                # Increment index for the next data point
                index += 1

        except KeyboardInterrupt:
            print("\nData collection stopped.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
