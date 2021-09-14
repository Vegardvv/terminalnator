# terminalnator
Containing both a CLI and GUI version is a script to deploy interface configuration to Cisco switches or routers.  

**Long Description**

Terminalnator is a series a script that create two versions of the same program, a CLI based and a GUI based. The goal of the terminalnator program is configure Cisco routers and switches remotley and efficiently through SSH. 

The program features file storage to save connections to devices for quick re-connection, ability to execute singular commands on the device and the main function which is take CSV spreadsheet with device interface attributes and create sets of commands and execute them all at once on the device.


**Requirements**

The program requries python 3.0 or higher to run, tested on python 3.8.5.

Netmiko https://github.com/ktbyers/netmiko

Install with "pip install netmiko"


**Usage**

CLI

Run script, select option with letter input. To connect to Cisco device, make sure the device has SSH setup. Use CSV files in program directory to create device configurations.


GUI

Running script bring up root window. Add connections or delete them. Select connection to connect to. Also make sure device has SSH setup and is reachable. Use same CSV files to make device configurations. Always use disconnect button in connection window to safely close the connection.
