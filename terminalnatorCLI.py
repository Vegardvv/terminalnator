#! /usr/bin/python3
# 13/04/21
# Vegard Haugvaldstad Vik
#
from terminalnatorclass import *


import os
import getpass


"""[CLI script]

        Serves as the CLI script for Terminalnator

    Functions
    ---------
    list_files
    get_config_from_file
    list_conns
    new_connection
    del_conn
    select_connection
    connection
"""

def get_config_from_file(files):
    """[Ask for file name input, if file name is present in directory, file is chosen
        Get input from user about device type, run relevant netssh class method for users choice]

    Returns:
        [str]: Returns list of commands which have been created using the Netssh class method for translating spreadsheet into Cisco readable commands.
        [bool] Return False if user does a Keyboardinterrupt
    """
    print("Write full file name of the config CSV file")
    file_choice = True
    while file_choice:                                                                                                      # While loop to take inputs untill valid file input is done
        try:
            file_input = input(": ")
        except KeyboardInterrupt:
            return None
        if file_input in files:
            break
        else:
            print("File not found, try again")

    print("Specify device type (r)outer or (s)witch")
    device_choice = True
    while device_choice:
        try:
            device_type = input(": ")
        except KeyboardInterrupt:
            return None                           
        if device_type == 's':
            return netssh.load_switch_config(file_input)                                                                    # Run CSV method with file name and return string of commands
            
        if device_type == 'r':
            return netssh.load_router_config(file_input)

        else:
            print("Please input one of the device options")

def list_conns():
    """Load connections with netssh class method, iterate through storage and print connection list
    """
    netssh.load_conn()                                                                                                      # Load connections from file
    conn_list = []
    for n in netssh.storage:
        conn_list.append(f"Host:{n.host}:{n.port} - Connection ID:{n.connection_id}")
    
    print("-------------------\n")
    print("Saved connections:")
    for c in conn_list:
        print(c)
    print("\n-------------------")

def new_connection():
    """Takes user input to make a new instance with the netssh object, 
       save new connections and print list of available connections

    
    """
    print("Enter the host address, SSH username and port to the Cisco device")
    try:
        host = input("Host: ")
        username = input("Username: ")
        port = input('Port: ')
    except KeyboardInterrupt:
        return None
    netssh(host, username, port)
    netssh.save_conn()
    print("New connection added:")
    list_conns()

def del_conn():
    """With an input of a connection id, netssh class method is ran with parameter

    Args:
        id ([int]): [Connection id to delete]
    """
    print("Input ID of connection to delete")
    list_conns()  
    try:
        id_input = int(input("Delete?: "))
    except KeyboardInterrupt:
        return None
    netssh.delete_conn(id_input)
    netssh.save_conn()
    list_conns()        

def select_connection():
    """Print connections and ask for id input to return

    Returns:
        [object]: [Object instance of selected Id]
    """
    list_conns()
    print("Input id of host to connect")
    select = True
    while select:
        try:
            id_input = int(input(": "))
        except KeyboardInterrupt:
            return None
        for n in netssh.storage:                                                                                            # If id is found, input is valid
            if id_input == n.connection_id:                             
                id = n
                return id
        else:
            print("Id is not in list, input again.")
    
def connection(conn):
    """Ask user for passwords input using getpass to hide terminal prompt


    Args:
        conn ([object]): [Object instance of netssh]

    Returns:
        [bool]: [Return True if connection is successfull]
    """
    if conn == None:
        return None
    login = True
    print("Please enter password to login through SSH and then the password to enable configuraton on the device:")
    while login:
        try:
            SSH_pass = getpass.getpass("SSH Password\n: ")                                                                  # Using getpass to obscure user input
            enable_pass = getpass.getpass("Enable Password\n: ")
        except KeyboardInterrupt:
            return None
        try:
            print("\nConnecting to device...\n")
            conn.connect(SSH_pass, enable_pass)                                                                             # Use instance to iniate connection to Cisco device with inputed passwords
            return True
        except Exception as e:                                                                                              # Print error information if connection fails
            print(e)
            print("Please make sure the device is on,")
            print("SSH is activated or try inputting passwords again: \n")

        except KeyboardInterrupt:
            print("Keyboard interrupt detected! Exiting to main menu...\n")
            login = False

menu = """Choose an option:
        l - List connections
        d - Delete a connection
        n - New connection
        c - Connect to a Cisco device
        o - Show options
        q - Exit program"""

sub_menu = """ Choose an option:
        c - Send single command
        l - List files in directory
        f - Import configuration from file and execute
        s - Save current configuration on device
        o - Show options
        d - Disconnect from device and exit to main menu"""

print("Terminalnator")
root = True
while root:                                                                                                                 # User options
    print(menu)
    try:
        select = input(": ")                                                                                                # Input to select option
    except KeyboardInterrupt:
        print("Keyboard interrupt detected! Exiting...\n")
        select = 'q'

    if select == 'l':
        list_conns()

    elif select == 'd':                                                                                                     # Try to delete connection if exists, if not go back to main menu
        del_conn()
        
    elif select == 'n':
        new_connection()
        
    elif select == 'c':
        conn = select_connection()

        if connection(conn) == True:                                                                                        # If connection is successfull, sub-menu is shown with options
            print(f'Connected to {conn.host}:{conn.port} - {conn.username}')
            print(sub_menu)
            conn_loop = True
            while conn_loop:
                try:
                    conn_select = input(": ")
                except KeyboardInterrupt:
                    print("Keyboard interrupt detected! Exiting...\n")
                    conn_select = 'd'
                    
                if conn_select == 'c':                                                                                      # User input for command to execute on device
                    print("Input command")
                    try:
                        com = input(": ")
                    except KeyboardInterrupt:
                        print("Keyboard interrupt detected! Exiting...\n")
                        conn.disconnect()
                        conn_loop = False
                    print(conn.command(com))


                elif conn_select == 'l':
                    print(os.listdir())

                elif conn_select == 'f':
                    files = os.listdir()
                    print(files)
                    config = get_config_from_file(files)
                    print(conn.config_command(config))

                elif conn_select == 's':
                    print(conn.save_command())

                elif conn_select =='o':
                    print(sub_menu)

                elif conn_select == 'd':
                    print("Disconnecting...")
                    conn.disconnect()
                    conn_loop = False

    elif select == 'o':
        print(menu)

    elif select == 'q':
        print("Exiting...")
        root = False
    
    else:
        print("Invalid input, try again")
    