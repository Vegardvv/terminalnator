#! /usr/bin/python3
# 13/04/21
# Vegard Haugvaldstad Vik
#
import pickle
import csv
from netmiko import ConnectHandler

"""
    Purpose
    -------

    Create object instances that will hold the value of connection details to Cisco Switches and Routers.
    Object can be used to connect to, send singular and list of commands to Cisco devices.
    Holds static methods that faciliate the connection with ability to save to file, load to file and delete specific instances.
    Holds static methods that can content of CSV files to list of commands that can be used with command method.

    """

class netssh:
    """[Create and maintain connections]

    
    """
    storage = []                                                                                                            # Storage for instances which can be saved to file

    def __init__(self, host, username, port):
        """[Connection object]

        Args:
            host ([str]): [IP or hostname address of Cisco device]
            username ([str]): [Username to authenticate with SSH]
            port ([int]): [Port number that SSH service is using]
        """
        
        self.host = host                                                                                                    # Host address to connect
        self.username = username                                                                                            # Device username for authentication
        self.port = port                                                                                                    # Port that device SSH service is running on
        self.connection_id = 100                                                                                 
        self.check_id()                                                                                                     # Unique ID to differentiate instances
        self.__class__.storage.append(self)                                                                                 # Append instance to storage list

    def check_id(self):
        """[Method to create unique ID's in object instance creation]
        """
        check = 0
        for i in __class__.storage:                                                                                         # Count number of instances
            check += 1

        while check != 0:                                                                                                   # Run for loop times the number of instances
            for i in __class__.storage:
                if i.connection_id == self.connection_id:                                                                   # Check if ID already is used, increment if true
                    self.connection_id += 1
            check -= 1


    def connect(self, password, secret):                                                                                    # Using Netmiko module, makes a connect handle using instance
        """[Method to use Netmiko connection maker to Cisco device SSH server]

        Args:
            password ([str]): [Password to authenticate with SSH]
            secret ([str]): [Password to authenticate to configuration mode on device]
        """
                                                                                                                            # Passwords are not in object for security reasons
        self.net_connect = ConnectHandler(device_type='cisco_ios', host=self.host, 
        username=self.username, port=self.port, password=password, secret=secret) 

    def disconnect(self):                                                                                                   # Disconnect Connect handler session
        """[Disconnet from SSH session]
        """
        self.net_connect.disconnect()

    def command(self, cmd):                                                         
        """[Input to command to execute on device]

        Args:
            cmd ([str]): [Inputted string executed to device]

        Returns:
            [str]: [Returns string of output from device]
        """ 
        self.net_connect.enable()                                                                                           # Enable configuration mode on device
        output=self.net_connect.send_command(cmd)
        return output

    def config_command(self, list):
        """[Input to command to execute on device]

        Args:
            list ([list]): [Inputted list executed to device]

        Returns:
            [str]: [Returns string of output from device]
        """
        self.net_connect.enable()
        output=self.net_connect.send_config_set(list)
        return output
    
    def save_command(self):
        """[Input to command to execute on device]

        Returns:
            [str]: [Return output of device]
        """
        self.net_connect.enable()
        output=self.net_connect.send_command("write mem")
        return output


    @staticmethod
    def save_conn():
        """[Saves class storage to file with pickle]
        """
        f = open("sshconnections", "wb")
        pickle.dump(netssh.storage, f)
        f.close()
    
    @staticmethod
    def delete_conn(connection_id):
        """[Delete instance with inputed id]

        Args:
            connection_id ([int]): [id of object to delete]

        Returns:
            [bool]: [Returns False with invalid input]
        """

        try:
            for i in __class__.storage:                                                                                     # Calls instance from list and deletes it
                if i.connection_id == connection_id:
                    del __class__.storage[netssh.storage.index(i)]
                    del i
        except: 
            return False
                
    @staticmethod
    def load_conn():
        """[Load storage list from file with pickle]

        Returns:
            [bool]: [Returns True if storage list is already made in script]
        """
        if __class__.storage:
            return True
        else:
            try:
                f = open("sshconnections", "rb")                           
                pickle_load = pickle.load(f)
                for n in pickle_load:                                                                                       # Content is iterated through and appended to storage list
                    __class__.storage.append(n)
                f.close()

            except FileNotFoundError:                                                                                       # If File is missing, create and open new file
                f = open("sshconnections", "wb")
                f.close()
            
            except EOFError:                                                                                                # If File content is missing, create and open new file
                f = open("sshconnections", "wb")
                f.close()


    @staticmethod
    def load_switch_config(filename):
        """[Opens CSV file and append content to dictonary. Creates commands from dictonary and append to list]

        Args:
            filename ([str]): [Enter name of file which will open in string format]

        Returns:
            [list]: [Returns list with configuration commands.]
        """
        with open(filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            next(reader)                                                                                                    # Skip first line which is keywords
            config = []
            for line in reader:
                config.append(f"interface {line['Interface']}")
                config.append(f"description {line['Description']}")
                if line['Vlan_id'] != 'None':                                                                               # If row contains 'None' on Vlan_id, only append 'trunk' on switchport mode 
                    config.append(f"switchport mode {line['Switchport_mode']}")
                    config.append(f"switchport access vlan {line['Vlan_id']}")
                else:
                    config.append(f"switchport mode trunk")
                config.append("no shutdown")
            return config

    @staticmethod
    def load_router_config(filename):
        """[Opens CSV file and append content to dictonary. Creates commands from dictonary and append to list]

        Args:
            filename ([type]): [description]

        Returns:
            [type]: [description]
        """
        with open(filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            next(reader)                                                                                                    # Skip first line which is keywords
            config = []
            for line in reader:
                config.append(f"interface {line['Interface']}")
                config.append(f"description {line['Description']}")
                config.append(f"ip address {line['IP']} {line['Netmask']}")
                if line['Vlan_id'] != 'None':                                                                               # Will only append string with command for vlan if other than zero.
                    config.append(f"encapsulation dot1q {line['Vlan_id']}")
                config.append("no shutdown")
            return config
