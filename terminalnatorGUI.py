#!/usr/bin/python3
# 13/04/21
# Vegard Haugvaldstad Vik
#
from terminalnatorclass import *

from tkinter import *
from tkinter.filedialog import askopenfilename
    
"""[GUI script]

        Serves as the Graphical interface script for Terminalnator

    Classes
    ---------
    configGUI
"""

class configGUI:
    """Create tkinter window for GUI, along with adding the widgets, functionality to the buttons and Toplevel windows

    """

    def __init__(self, root, title, geometry, color):
        """Root window for the GUI, takes values for window's attributes
           Has listbox where connections are shown, button to connect to specific connections
           Button to delete connections and button to add new connections

        Args:
            root ([class]): [As root is assigned to the tkinter class it serves as the loop to maintain the window]
            title ([str]): [Title of window]
            geometry ([str]): [Size of window; example '100x100']
            color ([str]): [Color of window's background]
        """
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.configure(bg=color)
        

        self.conns_frame = Frame(root)                                                                                      # Frames are used to group widgets in the window together
        self.conns_frame.grid(column=0, row=0, padx=5 ,pady=5)                                                              # Placement of frames are done with the grid system, every placement has 5 pixels each direction for visual leeway

        self.saved_conns = Listbox(self.conns_frame)
        self.saved_conns.pack(side=LEFT, padx=5, pady=5)

        self.connect_btn = Button(self.conns_frame, text="Connect", command=self.authentication)
        self.connect_btn.pack(side=RIGHT, padx=5, pady=5)

        self.delete_btn = Button(self.conns_frame, text="delete", command=self.del_conn)
        self.delete_btn.pack(side=RIGHT, padx=5, pady=5)

        self.new_conn = Button(self.root, text="Add New Connection", command=self.new_connection)
        self.new_conn.grid(row=3)

        self.auther_label = Label(self.root, text="@Vegard Vik, 2021")
        self.auther_label.place(x=0, y=230)


    def list_conns(self):
        """Deletes old content of the listbox in the root window, and loads new connections using netssh method
        """
        self.saved_conns.delete(0, END)

        netssh.load_conn()

        listbox_num = 0
        for n in netssh.storage:                                                                                                            # Listbox entries has to be numbered to display properly
            listbox_num += 1                                                                                                                # Increment and print number value for each entry in list
            self.saved_conns.insert(listbox_num, f"{n.host}:{n.port}-{n.connection_id}")


    def new_connection(self):
        """Toplevel window for adding new connections by user
           Contains three elements consisting of label and entry field for host, username and port input
           Contains Button that activates method to take entry inputs and create new connection
        """
        self.new_conn_window = Toplevel()
        self.new_conn_window.title("New Connection")
        self.new_conn_window.geometry("250x175")
        self.new_conn_window.configure(bg='blue')


        self.host_frame = Frame(self.new_conn_window)
        self.host_frame.pack(padx=5, pady=5)

        self.host_label = Label(self.host_frame, text='Host')
        self.host_label.pack(side=LEFT, padx=5, pady=5)

        self.host_entry = Entry(self.host_frame)
        self.host_entry.pack(side=RIGHT, padx=5, pady=5)


        self.username_frame = Frame(self.new_conn_window)
        self.username_frame.pack(padx=5, pady=5)

        self.username_label = Label(self.username_frame, text='Username')
        self.username_label.pack(side=LEFT, padx=5, pady=5)

        self.username_entry = Entry(self.username_frame)
        self.username_entry.pack(side=RIGHT, padx=5, pady=5)

        self.port_frame = Frame(self.new_conn_window)
        self.port_frame.pack(padx=5, pady=5)

        self.port_label = Label(self.port_frame, text='Port') 
        self.port_label.pack(side=LEFT, padx=5, pady=5)

        self.port_entry = Entry(self.port_frame)
        self.port_entry.pack(side=RIGHT, padx=5, pady=5)

        self.new_conn_btn = Button(self.new_conn_window, text="Add Connection", command=self.add_new_conn)
        self.new_conn_btn.pack(padx=5, pady=5)


        self.new_conn_window.mainloop()


    def add_new_conn(self):
        """Class method for button in new_connection, creates netssh instance with inputs
        """

        netssh(self.host_entry.get(), self.username_entry.get(), int(self.port_entry.get()))

        self.host_entry.delete(0, END)                                                                                                      # Deletes entries present in new_connection entry field when button is pressed
        self.username_entry.delete(0, END)
        self.port_entry.delete(0, END)

        netssh.save_conn()                                                                                                                  # Save connections to file

        self.list_conns()


    def del_conn(self):
        """Method for delete button in root window, checks if connection id is in storage file and deletes the connection if so
           Saves current connections to storage file
        """
        for n in netssh.storage:
            if f"-{n.connection_id}" in self.saved_conns.get(self.saved_conns.curselection()):                                              # Checks if connection id in storage is in Listbox string
                netssh.delete_conn(n.connection_id)

        netssh.save_conn()
        self.list_conns()


    def authentication(self):
        """Class method for connect button in root window, makes variable out of relevant instance
           Has two elements with frames containing, label and entry for SSH password and enable configuration password for device
           Button to create the connection window
        """
        for n in netssh.storage:
            if f"-{n.connection_id}" in self.saved_conns.get(self.saved_conns.curselection()):
                self.dev_connect = n

        self.auth_window = Toplevel()
        self.auth_window.title(f"Authenticating: {self.dev_connect.host}:{self.dev_connect.port} - {self.dev_connect.username}")                    # Title of window is made using connection's host address and username 
        self.auth_window.geometry("495x75")
        self.auth_window.configure(bg='purple')


        self.auth_frame = Frame(self.auth_window)
        self.auth_frame.grid()


        self.password_label = Label(self.auth_frame, text="SSH Password")
        self.password_label.pack(side=LEFT, padx=5, pady=5)

        self.password_entry = Entry(self.auth_frame, show='*')
        self.password_entry.pack(side=LEFT, padx=5, pady=5)


        self.secret_label = Label(self.auth_frame, text="Enable mode password")
        self.secret_label.pack(side=LEFT, padx=5, pady=5)

        self.secret_entry = Entry(self.auth_frame, show='*')
        self.secret_entry.pack(side=LEFT, padx=5, pady=5)


        self.auth_btn = Button(self.auth_window, text='Authenticate', command=self.connection)
        self.auth_btn.grid(row=1, padx=5, pady=5)


        self.auth_window.mainloop


    def connection(self):
        """Class method for authentication window button
           Saves passwords as variable and connects to device
           Destroys the authentication and creates a new Toplevel window for the connection
           Contains four elements with individual frames various widgets

        """

        self.auth_pass = self.password_entry.get()
        self.auth_secret = self.secret_entry.get()

        self.auth_window.destroy()

        self.connect_window = Toplevel()
        self.connect_window.title(f"Connection: {self.dev_connect.host}:{self.dev_connect.port} - {self.dev_connect.username}")             # Title of window is made using connection's host address and username           
        self.connect_window.geometry("450x475")
        self.connect_window.configure(bg='black')

        try:
            self.dev_connect.connect(self.auth_pass, self.auth_secret)
            self.status_label = Label(self.connect_window, text='Connected')
            self.status_label.pack(padx=5, pady=5)
        except Exception as e:                                                                                                              # Print error information if connection fails
            self.status_label = Label(self.connect_window, text=e)
            self.status_label.pack(padx=5, pady=5)


        self.file_frame = Frame(self.connect_window)
        self.file_frame.pack(padx=5, pady=5)

        file_info = "Select CSV file to make configuration for device. \n Choose approriate device for configuration."
        self.file_info_label = Label(self.file_frame, text=file_info)
        self.file_info_label.pack(side=TOP, padx=5, pady=5)


        self.filename = StringVar()
        self.file_label = Label(self.file_frame, textvariable=self.filename)                                                                # Dynamic label of file name chosen
        self.file_label.pack(side=BOTTOM, padx=5, pady=5)

        self.file_type = StringVar()
        self.file_radio_1 = Radiobutton(self.file_frame, text="Switch", variable = self.file_type, value = 's')                             # Radio buttons that changes string of file_type variable
        self.file_radio_1.pack(side=LEFT, padx=5, pady=5)

        self.file_radio_2 = Radiobutton(self.file_frame, text="Router", variable = self.file_type, value = 'r')
        self.file_radio_2.pack(side=LEFT, padx=5, pady=5)

        self.file_radio_1.select()                                                                                                          # Makes default radio button selection to first one

        self.file_btn = Button(self.file_frame, text="Select file", command=self.conn_file_select)                        
        self.file_btn.pack(side=LEFT, padx=5, pady=5)

        self.exe_file_btn = Button(self.file_frame, text="Load", command=self.exe_file_config)                  
        self.exe_file_btn.pack(side=LEFT, padx=5, pady=5)

        
        self.cmd_frame = Frame(self.connect_window)
        self.cmd_frame.pack(padx=5,pady=5)

        self.cmd_info_label = Label(self.cmd_frame, text="Input singular command to execute to device.")
        self.cmd_info_label.pack(side=TOP, padx=5, pady=5)

        self.cmd_entry = Entry(self.cmd_frame)                                                                                              # Entry for command to execute to device
        self.cmd_entry.pack(side=LEFT, padx=5, pady=5)

        self.cmd_btn = Button(self.cmd_frame, text="Execute", command=self.conn_exe_cmd)
        self.cmd_btn.pack(side=LEFT, padx=5, pady=5)


        self.save_frame = Frame(self.connect_window)
        self.save_frame.pack(padx=5,pady=5)

        save_info = "Save current configuration or disconnect from device and close window"
        self.save_info_label = Label(self.save_frame, text=save_info)                                                                       # Execute save command to device
        self.save_info_label.pack(side=TOP, padx=5, pady=5)

        self.save_btn = Button(self.save_frame, text="Save", command=self.conn_save)
        self.save_btn.pack(side=LEFT, padx=5, pady=5)

        self.disc_btn = Button(self.save_frame, text="Disconnect", command=self.conn_disconnect)
        self.disc_btn.pack(side=LEFT, padx=5, pady=5)

        self.connect_window.mainloop


    def display_output(self, output):
        """Display window for class method with output from device

        Args:
            output ([str]): [Output from connected Cisco device]
        """
        self.display_window = Toplevel()
        self.display_window.title(f"Connection: {self.dev_connect.host}:{self.dev_connect.port} - {self.dev_connect.username}")

        self.output_label = Label(self.display_window, text=output)                                                             
        self.output_label.pack(padx=5, pady=5)

        self.display_window.mainloop


    def conn_exe_cmd(self):
        """Takes entry from connection window cmd_entry field and uses connection instance command method to execute command to device-
           With output of the command a new Toplevel window is executed to display output
        """
        self.display_output(self.dev_connect.command(self.cmd_entry.get()))


    def conn_file_select(self):
        """Set the filname stringvar to the filename of the configuration csv file using tkinter askopenfilname
        """
        self.filename.set(askopenfilename())                                                                                                # Use file explorer to select filename


    def exe_file_config(self):
        """Checks if the user has chosen an configuration file and then selects the device type according to radiobutton choice

        """
        if len(self.filename.get()) >= 1:                                                                                                   # Checks if a file name is actually selected
            if self.file_type.get() == 's':                                                                                                 # Executes different connection method depending on user's radio button choice
                self.config_list = self.dev_connect.load_switch_config(self.filename.get())
            elif self.file_type.get() == 'r':
                self.config_list = self.dev_connect.load_router_config(self.filename.get())
            else:
                return False
            self.display_output(self.dev_connect.config_command(self.config_list))                                                          # Send output to display window method
        else:
            return False                                                                                                                    # Do nothing if no file is selected


    def conn_save(self):
        """Send save command to device and sends output to display window method
        """
        self.display_output(self.dev_connect.save_command())


    def conn_disconnect(self):
        """Disconnects safely from device, destroys the instance of the connection object and destroys the connection window
        """
        self.dev_connect.disconnect
        del self.dev_connect
        self.connect_window.destroy()

root = Tk()
c = configGUI(root, 'Terminalnator', "265x250", 'green')                                                                                    # Launch root window with preffered attributes
c.list_conns()                                                                                                                              # list connections in listbox in root window


root.mainloop()