from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import configparser
import smtplib

Program = Tk()
# Global Variables
config = configparser.RawConfigParser()
config.read('config.ini')

# Tab Control
TabControl = ttk.Notebook(Program)
SendEmail = ttk.Frame(TabControl)
SendSMS = ttk.Frame(TabControl)
MultipleEmail = ttk.Frame(TabControl)
MultipleSMS = ttk.Frame(TabControl)
Bulk = ttk.Frame(TabControl)
BulkSpam = ttk.Frame(TabControl)
Settings = ttk.Frame(TabControl)


# Settings
SenderEmail = config.get('Settings', 'senderemail')
SenderPassword = config.get('Settings', 'senderpassword')
SMTPServer = config.get('Settings', 'smtpserver')
SpamValue = config.get('Settings', 'spamvalue')
SMTPort = config.get('Settings', 'SMTPort')
SMSGateway = config.get('Settings', 'SMSGateway')

# Contacts
ContactList = config.get('Contacts', 'Contact')

# Send Message Information
Message = 'e'
Subject = ''
Email = ''
Number = ''

###########################################################################
                # Settings and Widgets for each tab #
###########################################################################
def BulkTab():
    def bntSendClick():
        ListOfContacts = ContactList.split()
        for People in ListOfContacts:

            Subject = ''
            Message = txtMessage.get("1.0", END)
            try:
                server = smtplib.SMTP(SMTPServer, int(SMTPort))  # Setup connection with SMTP server
                server.starttls()  # Opens secure TLS connection with server
                server.login(SenderEmail, SenderPassword)  # Logins to Email
                SentMessage = 'Subject: {}\n\n{}'.format(Subject, Message)  # Setup format of how to send the Email
                server.sendmail(SenderEmail, People, SentMessage)  # Sends the Email
                server.quit()  # Disconnects from the server
                messagebox.showinfo("SENT", "Email Sent!")  # Tells user that email was sent

            except:
                messagebox.showinfo("ERROR", "One or more Emails failed to send!")  # If email didn't send, Display this message

    LbMessage = Label(Bulk, text='Message').place(x=5, y=10)
    txtMessage = Text(Bulk, width=59, height=25)
    txtMessage.place(x=10, y=30)
    btnSend = Button(Bulk, width=10, text='Send', command=bntSendClick).place(x=10, y=440)
    lbHelpMessage=Label(Bulk, text='This will send messages to ALL contacts', fg="red").place(x=90, y=450)

def BulkSpamTab():
    def btnSendClick():
        ListOfContacts = ContactList.split()

        for People in ListOfContacts:


            Subject = ''
            Message = txtMessage.get("1.0", "end-1c")
            x = 0
            try:
                server = smtplib.SMTP(SMTPServer, int(SMTPort))
                server.starttls()
                server.login(SenderEmail, SenderPassword)
                SentMessage = 'Subject: {}\n\n{}'.format(Subject, Message)
                while x < int(SpamValue):
                    server.sendmail(SenderEmail, People, SentMessage)
                    x += 1
                    messagebox.showinfo("Sent", "Emails Sent!")
                server.quit()

            except:
                messagebox.showinfo("ERROR", "Email Failed to Send!")


    LbMessage = Label(BulkSpam, text='Message').place(x=5, y=10)
    txtMessage = Text(BulkSpam, width=59, height=25)
    txtMessage.place(x=10, y=30)
    btnSend = Button(BulkSpam, width=10, text='Send', command=btnSendClick).place(x=10, y=440)
    lbHelpMessage = Label(BulkSpam, text='This will send messages to ALL contacts', fg="red").place(x=90, y=450)

def SettingsTab():
    def btnSaveClick():
        Spam=SpamValueVariable.get()
        Email=SenderEmailVariable.get()
        Password=SenderPasswordVariable.get()
        smtpserver=SMTPServerVariable.get()
        Port=SMTPortVariable.get()
        Gateway=SMSGatewayVariable.get()
        Contact = txtContact.get("1.0", END)
        config.set('Settings', 'senderemail', Email)
        config.set('Settings', 'senderpassword', Password)
        config.set('Settings', 'smtpserver', smtpserver)
        config.set('Settings', 'spamvalue', Spam)
        config.set('Settings', 'SMTPort', Port)
        config.set('Settings', 'SMSGateway', Gateway)
        config.set('Contacts', 'Contact', Contact)
        with open('config.ini', 'w') as f:
            config.write(f)
        ContactList=Contact
        messagebox.showinfo("Saved", "Settings Saved!")

    # Spam Variable
    SpamValueVariable = StringVar() # Creates String Variable
    SpamValueVariable.set(SpamValue) # Sets Config files version of 'SpamValue' Into A String
    LbSpamVariable = Label(Settings, text='Spam Variable').place(x=5, y=10)
    txtSpamVariable = Entry(Settings, width=12, text=SpamValueVariable).place(x=10, y=30)

    # Sender Email
    SenderEmailVariable = StringVar()
    SenderEmailVariable.set(SenderEmail)
    LbSenderEmail = Label(Settings, text='Email').place(x=5, y=50)
    txtSenderEmail = Entry(Settings, width=35, text=SenderEmailVariable).place(x=10, y=70)

    # Sender Password
    SenderPasswordVariable = StringVar()
    SenderPasswordVariable.set(SenderPassword)
    LbSenderPassword = Label(Settings, text='Password').place(x=5, y=90)
    txtSenderPassword = Entry(Settings, width=25, text=SenderPasswordVariable).place(x=10, y=110)

    # SMTP Server
    SMTPServerVariable = StringVar()
    SMTPServerVariable.set(SMTPServer)
    LbSMTPServer = Label(Settings, text='SMTP Server').place(x=5, y=130)
    txtSMTPServer = Entry(Settings, width=40, text=SMTPServerVariable).place(x=10, y=150)
    # SMTP Port
    SMTPortVariable = StringVar()
    SMTPortVariable.set(SMTPort)
    LbPort = Label(Settings, text='Port').place(x=5, y=170)
    txtPort = Entry(Settings, width=5, text=SMTPortVariable).place(x=10, y=190)

    # SMS Gateway
    SMSGatewayVariable = StringVar()
    SMSGatewayVariable.set(SMSGateway)
    LbGateway=Label(Settings, text='SMS Gateway').place(x=5, y=210)
    txtGateway=Entry(Settings, width=30, text=SMSGatewayVariable).place(x=10, y=230)

    # Contacts
    LbContacts = Label(Settings, text='Contacts (Email)').place(x=5, y=250)
    txtContact = Text(Settings, width=59, height=10)
    txtContact.insert(INSERT, ContactList)
    txtContact.place(x=10, y=270)
    # Save Button
    btnSave = Button(Settings, width=10, height=0, text='Save', command=btnSaveClick).place(x=10, y=440)

def SendEmailTab():
    # function used when Send button is pressed
    def btnSendClick():
        # looks at what is in each textbox and stores it as a string
        Email=txtReceiverEmail.get("1.0","end-1c")
        Subject=txtSubject.get("1.0","end-1c")
        Message=txtMessage.get("1.0","end-1c")
        try:
            server = smtplib.SMTP(SMTPServer, int(SMTPort)) # Setup connection with SMTP server
            server.starttls() # Opens secure TLS connection with server
            server.login(SenderEmail, SenderPassword) # Logins to Email
            SentMessage='Subject: {}\n\n{}'.format(Subject, Message) # Setup format of how to send the Email
            server.sendmail(SenderEmail, Email, SentMessage) # Sends the Email
            server.quit() # Disconnects from the server
            messagebox.showinfo("SENT", "Email Sent!") # Tells user that email was sent

        except:
            messagebox.showinfo("ERROR", "Email Failed to Send!") # If email didn't send, Display this message
        SendEmailTab() # Calls this function to clear textboxes
    """
    Placing Labels and Textboxes
    Determining outcome of Button Pressed
    """
    # Receiver Email
    LbReceiverEmail = Label(SendEmail, text='To (email)').place(x=5, y=10)
    txtReceiverEmail = Text(SendEmail, width=59, height=0)
    txtReceiverEmail.place(x=10, y=30)
    # SMTP Server
    LbSubject = Label(SendEmail, text='Subject').place(x=5, y=50)
    txtSubject = Text(SendEmail, width=59, height=0)
    txtSubject.place(x=10, y=70)
    # Email Message
    LbMessage = Label(SendEmail, text='Message').place(x=5, y=90)
    txtMessage = Text(SendEmail, width=59, height=20)
    txtMessage.place(x=10, y=110)
    # Send Button
    btnSend = Button(SendEmail, width=10, height=0, text='Send', command=lambda: btnSendClick()).place(x=10, y=440)

def SendSMSTab():
    def btnSendClick():
        Number=txtReceiver.get("1.0","end-1c")
        Message=txtMessage.get("1.0","end-1c")
        try:
            server = smtplib.SMTP(SMTPServer, int(SMTPort))
            server.starttls()
            server.login(SenderEmail, SenderPassword)
            server.sendmail(SenderEmail, Number+SMSGateway, Message)
            server.quit()
            messagebox.showinfo("Sent", "SMS Sent!")
        except:
            messagebox.showinfo("ERROR", "SMS Failed to Send!")
        SendSMSTab()
    # Number
    LbReceiverNumber = Label(SendSMS, text='To (number)').place(x=5, y=10)
    txtReceiver = Text(SendSMS, width=59, height=0)
    txtReceiver.place(x=10, y=30)
    # Message
    LbMessage = Label(SendSMS, text='Message').place(x=5, y=50)
    txtMessage = Text(SendSMS, width=59, height=22)
    txtMessage.place(x=10, y=70)
    # Send Button
    btnSend = Button(SendSMS, width=10, height=0, text='Send', command=lambda: btnSendClick()).place(x=10, y=440)

def SpamEmailTab():
    def btnSendClick():
        Email = txtReceiverEmail.get("1.0", "end-1c")
        Subject = txtSubject.get("1.0", "end-1c")
        Message = txtMessage.get("1.0", "end-1c")
        x = 0
        try:
            server = smtplib.SMTP(SMTPServer, int(SMTPort))
            server.starttls()
            server.login(SenderEmail, SenderPassword)
            SentMessage = 'Subject: {}\n\n{}'.format(Subject, Message)
            while x < int(SpamValue):
                server.sendmail(SenderEmail, Email, SentMessage)
                x += 1
            server.quit()
            messagebox.showinfo("Sent", "Email Sent!")
        except:
            messagebox.showinfo("ERROR", "Email Failed to Send!")
        SpamEmailTab()
    # Receiver Email
    LbReceiverEmail = Label(MultipleEmail, text='To (email)').place(x=5, y=10)
    txtReceiverEmail = Text(MultipleEmail, width=59, height=0)
    txtReceiverEmail.place(x=10, y=30)
    # SMTP Server
    LbSubject = Label(MultipleEmail, text='Subject').place(x=5, y=50)
    txtSubject = Text(MultipleEmail, width=59, height=0)
    txtSubject.place(x=10, y=70)
    # Email Message
    LbMessage = Label(MultipleEmail, text='Message').place(x=5, y=90)
    txtMessage = Text(MultipleEmail, width=59, height=20)
    txtMessage.place(x=10, y=110)
    # Send Button
    btnSend = Button(MultipleEmail, width=10, height=0, text='Spam', command=lambda: btnSendClick()).place(x=10, y=440)

def SpamSmsTab():
    def btnSendClick():
        Number = txtReceiver.get("1.0", "end-1c")
        Message = txtMessage.get("1.0", "end-1c")
        x=0
        try:
            server = smtplib.SMTP(SMTPServer, int(SMTPort))
            server.starttls()
            server.login(SenderEmail, SenderPassword)
            while x < int(SpamValue):
                server.sendmail(SenderEmail, Number + SMSGateway, Message)
                x += 1
            server.quit()
            messagebox.showinfo("Sent", "SMS Sent!")
        except:
            messagebox.showinfo("ERROR", "SMS Failed to Send!")
        SpamSmsTab()
    # Number
    LbReceiverNumber = Label(MultipleSMS, text='To (number)').place(x=5, y=10)
    txtReceiver = Text(MultipleSMS, width=59, height=0)
    txtReceiver.place(x=10, y=30)
    # Message
    LbMessage = Label(MultipleSMS, text='Message').place(x=5, y=50)
    txtMessage = Text(MultipleSMS, width=59, height=22)
    txtMessage.place(x=10, y=70)
    # Send Button
    btnSend = Button(MultipleSMS, width=10, height=0, text='Send', command=lambda: btnSendClick()).place(x=10, y=440)

def TabControler():
    # Create 'Send Email' Tab
    TabControl.add(SendEmail, text="Send Email")
    # Create 'Send SMS' Tab
    TabControl.add(SendSMS, text="Send SMS")
    # Create 'Spam Email' Tab
    TabControl.add(MultipleEmail, text="Spam Email")
    # Create 'Spam SMS' Tab
    TabControl.add(MultipleSMS, text="Spam SMS")
    # Create 'Bulk' Tab
    TabControl.add(Bulk, text='Bulk')
    # Create 'Bulk Spam' Tab
    TabControl.add(BulkSpam, text='Bulk Spam')
    # Create 'Settings' Tab
    TabControl.add(Settings, text="Settings")

    # Pack Tabs
    TabControl.pack(expan=1, fill="both")  # Displays all tabs above


def Main():
    # Dashboard Setup
    Program.title('SMSPAM')# creates title for program
    Program.geometry('500x500')# sets geometry(size) for program
    Program.resizable(False, False)# Cant resize program

    # Setup for Tab Control
    SendEmailTab()
    SpamSmsTab()
    SpamEmailTab()
    SendSMSTab()
    TabControler()
    SettingsTab()
    BulkTab()
    BulkSpamTab()

# Runs main function
Main()

# Loops to allow creation of new widgets through entire project
mainloop()