# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 16:44:22 2020

@author: Valeria

NOT TESTED
This code write locally csv
upload in FTP
download In FTP
no mail

files used
http://127.0.0.1:5000/index
http://127.0.0.1:5000/newactivation
http://127.0.0.1:5000/submit

"""
from flask import Flask, request,flash,render_template
from flask_mail import Mail, Message #send mail
from ftplib import FTP
from time import sleep
from datetime import datetime
from datetime import timedelta
import csv
import os
import shutil
#...flash ...IMPROVEMENT in animation
app=Flask(__name__)
app.secret_key='secretkey'


serverName='43.249.199.51' 
username='sparkwbb'
password='+@)rKAeG}6!bNnp>'
FTPdirectoryIn='/43.249.199.51/Incoming' #Incoming or Incoming_ss
FTPdirectoryOut='/43.249.199.51/Outgoing'


'''
app.config.update(
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USE_TLS=False,
    MAIL_USERNAME = 'projectsender20@gmail.com',
	MAIL_PASSWORD = '123abc!@#'
	)
mail = Mail(app)
'''

def send_mail_good():
	try:
		msg = Message("RES2 received", 
        sender="projectsender20@gmail.com",
		recipients=["projectsender20@gmail.com"])
		msg.body = "Hello!"  
#        msg.html = "<b>testing</b>"         
		mail.send(msg)
		return 'Mail sent!>good news'
	except Exception as e:
		return(str(e)) 

def check_reply(Account):
    fileNameMail = 'WNN'+str(Account)+'_RES2.csv'
    filePathMail=os.path.join('Outgoing',fileNameMail)#folder where the RES2.csv is saved
    datalist=[]
    with open(filePathMail, mode='r') as csv_file:
        csv_reader=csv.reader(csv_file)
        header=next(csv_reader) #go in second line, also next(csv_reader)
        datalist=[row for row in csv_reader]
        data=datalist[0]
        return (data)

def send_mail_good_activation(Account,filePathOut,fileNameOut,res2info):
# retrieve Inconming information    
    fileName = 'WNN'+str(Account)+'.csv'
    filePathIn=os.path.join('Incoming',fileName)
    with open(filePathIn, mode='r') as csv_file:
        csv_reader=csv.reader(csv_file)
        header=next(csv_reader) #go in second line, also next(csv_reader)
        datalist=[row for row in csv_reader]
        data=datalist[0]      
        SIMNo=data[8]
        ProductOfferID=data[9]
        ReqType=data[0]
        
        
    try:
        #send your message with credentials specified above
        msg = Message("Reply - Customer Account No: " + str(Account)+" - Request type: "+ ReqType + " - Status: "+ str(res2info[7]) ,        
                      sender="projectsender20@gmail.com",		
                      recipients=["projectsender20@gmail.com"])
        with app.open_resource(filePathOut) as fp:
            msg.attach(fileNameOut,'text/csv',fp.read()) 
            
        if str(res2info[7]) == 'Complete':
            msg.body = "\n\n\n            Replay form Spark, Customer Account No: {}\n\n\n\
            Mobile Number: {}\n            SIMNo: {}\n            External Batch Id: {}\n            Siebel Order Number: {}\n\n\n\
            Request type: {}\n            Spark Plan: {}\n\n\n\
            The Status is: {}\n\n\n\n"\
            .format(Account,res2info[6],SIMNo, res2info[3],res2info[2],ReqType, ProductOfferID, res2info[7])
                  
#        elif res2info[8]=="": #not details are present
#            msg.body = "\n\n\n            Replay form Spark, Customer Account No: {}\n\n\n\
#            Mobile Number: {}\n            SIMNo: {}\n            External Batch Id: {}\n            Siebel Order Number: {}\n\n\n\
#            Request type: {}\n            Spark Plan: {}\n\n\n\
#            The Status is: {}\n\n\n\n"\
#            .format(Account,res2info[6],SIMNo, res2info[3],res2info[2],ReqType, ProductOfferID, res2info[7])
            
        else:
            msg.body = "\n\n\n            Replay form Spark, Customer Account No: {}\n\n\n\
            Mobile Number: {}\n            SIMNo: {}\n            External Batch Id: {}\n            Siebel Order Number: {}\n\n\n\
            Request type: {}\n            Spark Plan: {}\n\n\n\
            The Status is: {}\n\n\n\n            Error Description is: {}\n\n\n\n"\
            .format(Account,res2info[6],SIMNo, res2info[3],res2info[2],ReqType, ProductOfferID, res2info[7], res2info[8])
            
       
        mail.send(msg)
        


        # tell the script to report if your message was sent or which errors need to be fixed 
        print('Sent')        
    except Exception as e:
        return(str(e))
        
def send_mail_incoming(Account,filePathIn,fileNameIn):
    try:
        #send your message with credentials specified above
        msg = Message("Incoming file Customer Account No " + str(Account),        
                      sender="projectsender20@gmail.com",		
                      recipients=["projectsender20@gmail.com"])
        with app.open_resource(filePathIn) as fp:
            msg.attach(fileNameIn,'text/csv',fp.read()) 
        mail.send(msg)

        # tell the script to report if your message was sent or which errors need to be fixed 
        print('Sent') 
        return 1
    except Exception as e:
        return(str(e))
        
        
def send_mail_bad(Account):
	try:
		msg = Message("Reply for Customer Account No " + str(Account)+" IS NOT CREATED", 
                sender="projectsender20@gmail.com",
                recipients=["projectsender20@gmail.com"])
		msg.body = "Some problem arise in processing the request for Customer Account No "+ str(Account)+  " TRY AGAIN!"
		mail.send(msg)
		return 'Mail sent!>Time expired! The file _RES2.csv is NOT present within xx minutes'
	except Exception as e:
		return(str(e)) 

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/newactivation', methods=['POST','GET'])
@app.route('/newactivation.html', methods=['POST','GET'])
@app.route('/newactivationwtf', methods=['POST','GET'])
@app.route('/newactivationwtf.html', methods=['POST','GET'])
@app.route('/newactivationflask', methods=['POST','GET'])
@app.route('/newactivationflask.html', methods=['POST','GET'])

#insert data in form
def form_example():
    error = None
    
    CustomerAccountNo=""
    SIMNo=""
    ELID=""

    if request.method=='POST':
        CustomerAccountNo = request.form.get('CustomerAccountNo')#can be None
        SIMNo = request.form.get('SIMNo')
        ELID = request.form.get('ELID')
        ProductOfferID = request.form.get('ProductOfferID')

        if CustomerAccountNo == None or  ELID == None or  SIMNo == None or  ProductOfferID == None:
            error = 'Invalid input'
            flash('Please fill all the fields', category='AllFields')
            if CustomerAccountNo == None:
                flash('Please fill this data ', category='CustomerAccountNosms')
            if SIMNo == None:
                flash('Please fill this data ', category='SIMNosms')
            if ELID == None:
                flash('Please fill this data ', category='ELIDsms')
            if ProductOfferID == None:
                flash('Please select an option', category='ProductOfferIDsms')

        
        if CustomerAccountNo == "" or SIMNo == "" or ELID == "" or  ProductOfferID == "" :
            error = 'Invalid input'
            flash('Please fill all the fields', category='AllFields')
            if CustomerAccountNo == "":
                flash('Please fill this data ', category='CustomerAccountNosms')
            if SIMNo == "":
                flash('Please fill this data ', category='SIMNosms')
            if ELID == "":
                flash('Please fill this data ', category='ELIDsms')
            if ProductOfferID == "":
                flash('Please select an option', category='ProductOfferIDsms')


        if len(CustomerAccountNo) != sum(c.isdigit() for c in CustomerAccountNo) and CustomerAccountNo != "":  
            error = 'Invalid input'             
            flash('Inserted data has {} digits and {} others characters'\
                  .format(sum(c.isdigit() for c in CustomerAccountNo),len(CustomerAccountNo)-sum(c.isdigit() for c in CustomerAccountNo)), category='CustomerAccountNosms')
            flash('Customer Accoun No should have just digits', category='CustomerAccountNosms')
          

 
        if [len(SIMNo),sum(c.isdigit() for c in SIMNo)] != [17,17] and SIMNo != "":
            error = 'Invalid input'             
            flash('Error details in SIM No', category='SIMNosms')
            flash('Inserted data has {} digits and {} others characters'\
                  .format(sum(c.isdigit() for c in SIMNo),len(SIMNo)-sum(c.isdigit() for c in SIMNo)), category='SIMNosms')
            flash('SIM No should have 17 digits', category='SIMNosms')



        if [len(ELID),sum(c.isdigit() for c in ELID)] != [9,9] and ELID != "":  
            error = 'Invalid input'             
            flash('Inserted data has {} digits and {} others characters'\
                  .format(sum(c.isdigit() for c in ELID),len(ELID)-sum(c.isdigit() for c in ELID)), category='ELIDsms')
            flash('ELID should have 9 digits', category='ELIDsms')
            
#  
        
        if error != None:
            return render_template('newactivation.html', error=error)
        

        temp = ProductOfferID.split()        
        ProductOfferID = temp[0]



#wirte the file.csv, TO DO: if not make ERROR message
        fileNameTemplate = 'WNNDDMMYY_Activate_EXAMPLE.csv'
        filePathTemplate=os.path.join('CSVTemplate',fileNameTemplate) #to handle windows and linux same way

        with open(filePathTemplate, mode='r') as csv_file:                      
            csv_reader=csv.reader(csv_file)
            header=next(csv_reader) #go in second line, also next(csv_reader)
            datalist=[row for row in csv_reader]
            data=datalist[0]
        data[3]='WNN'+str(CustomerAccountNo)
        data[8]=str(SIMNo)
        data[9]=str(ProductOfferID)
        data[30]=str(ELID)

        fileName = 'WNN'+str(CustomerAccountNo)+'.csv'
        filePathIn=os.path.join('Incoming',fileName) #to handle windows and linux same way
        filePathWaiting=os.path.join('Waiting',fileName)

#write .csv file locally       TO DO: if not make ERROR message, if yes make an OK message  
#INSERT: if the file is not in waiting folder. If the file is in waiting folder, not write it and send a message to wait
        with open(filePathIn, mode='w') as csv_file:
            csv_writer=csv.writer(csv_file,lineterminator='\r')
            csv_writer.writerow(header)
            csv_writer.writerow(data)
        shutil.copy(filePathIn, filePathWaiting)

    
#connect to the FTP server and write file, TO DO: if not make ERROR message,  if yes make an OK message  ?
        ftp = FTP(serverName)    
        ftp.login(username,password)   
        ftp.cwd(FTPdirectoryIn)
#open the local 'WNN'+str(CustomerAccountNo)+'.csv'
        with open(filePathIn, "rb") as f:
            ftp.storbinary('STOR ' + fileName, f,1024)
        ftp.cwd('/..')

        ftp.quit()


    
        return render_template('submit.html',error=error)
    
    return render_template('newactivation.html', error=error)



if __name__== '__main__':
    app.run(debug=True)
        
  

