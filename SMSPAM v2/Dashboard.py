from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import configparser
import smtplib

Program = Tk()
# Global Variables
config = configparser.RawConfigParser()
config.read('config.ini')
TabControl = ttk.Notebook(Program)
SendEmail = ttk.Frame(TabControl)
SendSMS = ttk.Frame(TabControl)
MultipleEmail = ttk.Frame(TabControl)
MultipleSMS = ttk.Frame(TabControl)
Settings = ttk.Frame(TabControl)
# Send Message Information
Message = ''
Subject = ''
Email = ''
Number = ''
SenderEmail = config.get('Main', 'senderemail')
SenderPassword = config.get('Main', 'senderpassword')
SMTPServer = config.get('Main', 'smtpserver')
SpamValue = config.get('Main', 'spamvalue')
SMTPort = config.get('Main', 'SMTPort')
SMSGateway = config.get('Main', 'SMSGateway')
AllowTLS = BooleanVar()
AllowTLS.set(bool(config.get('Main', 'SenderEmail')))

# Function used to create widgets and determined outcome of buttons pressed
def SettingsTab():
    def btnSaveClick():
        Spam=SpamValueVariable.get()
        Email=SenderEmailVariable.get()
        Password=SenderPasswordVariable.get()
        smtpserver=SMTPServerVariable.get()
        Port=SMTPortVariable.get()
        Gateway=SMSGatewayVariable.get()
        config.set('Main', 'senderemail', Email)
        config.set('Main', 'senderpassword', Password)
        config.set('Main', 'smtpserver', smtpserver)
        config.set('Main', 'spamvalue', Spam)
        config.set('Main', 'SMTPort', Port)
        config.set('Main', 'SMSGateway', Gateway)
        with open('config.ini', 'w') as f:
            config.write(f)
        messagebox.showinfo("Saved", "Settings Saved!")
    # Spam Variable
    SpamValueVariable = StringVar()
    SpamValueVariable.set(SpamValue)
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

    # Save Button
    btnSave = Button(Settings, width=10, height=0, text='Save', command=btnSaveClick).place(x=10, y=440)

# Function used to create widgets and determined outcomes of buttons pressed
def SendEmailTab():
    def btnSendClick():
        Email=txtReceiverEmail.get("1.0","end-1c")
        Subject=txtSubject.get("1.0","end-1c")
        Message=txtMessage.get("1.0","end-1c")
        try:
            server = smtplib.SMTP(SMTPServer, int(SMTPort))
            server.starttls()
            server.login(SenderEmail, SenderPassword)
            SentMessage='Subject: {}\n\n{}'.format(Subject, Message)
            server.sendmail(SenderEmail, Email, SentMessage)
            server.quit()
            messagebox.showinfo("Sent", "Email Sent!")
        except:
            messagebox.showinfo("ERROR", "Email Failed to Send!")
        SendEmailTab()
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

# Function used to create widgets and determined outcomes of buttons pressed
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

# Function used to create widgets and determined outcomes of buttons pressed
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

# Function used to create widgets and determined outcome of buttons pressed
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

# Function used to create widgets and determined outcome of buttons pressed
def TabControler():
    # Create 'Send Email' Tab
    TabControl.add(SendEmail, text="Send Email")
    # Create 'Send SMS' Tab
    TabControl.add(SendSMS, text="Send SMS")
    # Create 'Spam Email' Tab
    TabControl.add(MultipleEmail, text="Spam Email")
    # Create 'Spam SMS' Tab
    TabControl.add(MultipleSMS, text="Spam SMS")
    # Create 'Settings' Tab
    TabControl.add(Settings, text="Settings")
    # Pack Tabs
    TabControl.pack(expan=1, fill="both")  # Displays all tabs above

# Function used to create widgets and determined outcome of buttons pressed
def Main():
    # Dashboard Setup
    Program.title('SMSPAM')
    Program.geometry('500x500')
    Program.resizable(False, False)
    # Setup for Tab Control
    SpamSmsTab()
    SpamEmailTab()
    SendSMSTab()
    TabControler()
    SettingsTab()
    SendEmailTab()

# Runs main function
Main()

# Loops to allow creation of new widgets through entire project
mainloop()