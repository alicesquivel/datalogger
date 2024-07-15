# InfluxDB and Telegraf in Chameleon node

### Installing InfluxDB on Ubuntu 22.04 (x86_64)
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
Edit the /lib/systemd/system/influxdb.service file to pass the variables to the ```ExecStart``` value:
```
ExecStart=/usr/bin/influxd $ARG1 $ARG2
```

## Step-by-Step Instructions
Edit the ```/etc/default/influxdb2``` File:

This file allows you to set environment variables that the InfluxDB service will use.
```
sudo nano /etc/default/influxdb2
```
Add your custom configuration directives. For example:
```
ARG1="--http-bind-address=:8087"
ARG2="--storage-wal-fsync-delay=15m"
```
Save and close the file (Ctrl+O, Enter, Ctrl+X).

Edit the ```influxdb.service``` File:

Open the systemd service file to pass the variables to the ExecStart value.
```
sudo nano /lib/systemd/system/influxdb.service
```
Modify the ```ExecStart``` line to use the environment variables. For example, change:
```
ExecStart=/usr/lib/influxdb/scripts/influxd-systemd-start.sh
```
To:
```
ExecStart=/usr/bin/influxd $ARG1 $ARG2
```
The complete service file might look like this after modification:
```
[Unit]
Description=InfluxDB is an open-source, distributed, time series database
Documentation=https://docs.influxdata.com/influxdb/
After=network-online.target

[Service]
User=influxdb
Group=influxdb
LimitNOFILE=65536
EnvironmentFile=-/etc/default/influxdb2
ExecStart=/usr/bin/influxd $ARG1 $ARG2
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

[Install]
WantedBy=multi-user.target
Alias=influxd.service
```
Save and close the file (Ctrl+O, Enter, Ctrl+X).
Reload systemd and Restart the Service:
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
### Summary 
Edit ```/etc/default/influxdb2``` to add custom configuration options.
Edit ```/lib/systemd/system/influxdb.service``` to include the environment variables in the ExecStart line.
Reload systemd and restart the InfluxDB service to apply the changes.
Verify the service status to ensure it is running with the new configuration.
This process ensures that your InfluxDB service uses the custom configuration options defined in the ```/etc/default/influxdb2``` file. The service file references the environment file, and the ```ExecStart``` directive uses the environment variables to configure InfluxDB.
