# -*- coding: utf-8 -*-
"""
Created on Sun May 15 17:43:57 2022

@author: ravik
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 10:19:03 2022

@author: ravik
"""
import pandas as pd
import numpy as np
import string
from datetime import timedelta
import razorpay
import requests
import json
import os
import random
from flask import *
from random import randint
import pyrebase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib
fedral_secret='U8tK1tR6qC1jS2jI7aA4oR4hA7gG3mD2jF6fG6bS5eA4lU7hU6'
fedral_id='ef50018e-ff96-4f2c-9922-5a0f701ae690'
verifiy_cashfree_id="CF156734C9G4SCRG1A0QGEN8J5U0"
verifiy_cashfree_secret="f0055f8f1244d176e70becf9c9327fd97b5e872b"
key_id='141630a4daf9ae2a6912f8d696036141'
key_id_payout='CF141630C8JRNIBG1A0QGEN8ISFG'
secret_payout='ee3d2d056017a5d58ee9779ac78f5556561289f0'
secret='1b08e97659cb965064b5f59cbd7aeeb839e72f41'
#key_id='rzp_test_CCrR2VxczZ0INm'
#secret='zHSpEM0TArX5EPaBJ1K01kJV'
base64token= key_id+':'+secret
print(base64token)
t= 'Basic'+base64token
client = razorpay.Client(auth=(key_id, secret))
config = {
  "apiKey": "AIzaSyBHB-WVjph1-F7lUgUzox9jWM-cOn-wdjY",
  "authDomain": "razorpay-credit.firebaseapp.com",
  "databaseURL": "https://razorpay-credit-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "razorpay-credit.appspot.com"
}

app.secret_key ='464f31e17c630e6c094b5a04050b5f612c13df1f76ba015005101454be70db25'
auth_token='cnpwX3Rlc3RfQ0NyUjJWeGN6WjBJTm06ekhTcEVNMFRBclg1RVBhQkoxSzAxa0pW'
i=0
w=0
p=0
a=0
b=0
payment_id=""
transfer_id=''
order_id=''
amountinput=0
result=""
constantno="const_"
while(1):
    i=i+1
    a=randint(0,9)
    c= str(a)
    result=result+c
    if(i==10):
        break
while(1):
    p=p+1
    b=randint(0,9)
    d= str(b)
    constantno=constantno+ d
    if(p==6):
        break
static_dir = str(os.path.abspath(os.path.join(path="cashfree site")))
app = Flask(__name__, static_folder=static_dir,
            static_url_path="", template_folder=static_dir)
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app.config['SECRET_KEY'] = '464f31e17c630e6c094b5a04050b5f612c13df1f76ba015005101454be70db25'
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=60)

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": "","account_id":"","contact_id":"","amount":"","kyc":""}
temporary_details={}
def sendmail(reciep,body,subject):
    msg = MIMEMultipart()
    sender = "support@cardtobank.net"
    username = "support@cardtobank.net"
    password = "Sreedhar@123"
    host = "smtp.ionos.com"
    port = 587
    recipient=reciep
    body = body
    msg = MIMEMultipart()
    msg.add_header("From", sender)
    msg.add_header("To", recipient)
    msg.add_header("Subject", subject)
    msg.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()
# creating website pages
@app.route("/")
def login():
    if 'identification' in session:
            return redirect(url_for('welcome'))
    else:
        
     return render_template("Home.html")
@app.route("/sessionended",methods=['GET','POST'])
def login_home():
     return render_template("Home.html")
@app.errorhandler(404)
def error404page(e):
    return render_template('404.html')
#signout
@app.route("/signout")
def signoutuser():
    session.pop('identification',None)
    session.pop('name',None)
    return render_template("Home.html")
#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")
#login
@app.route("/login")
def loginuser():
    if 'identification' in session:
            return redirect(url_for('welcome'))
    else:
        return render_template("login.html")

@app.route("/payment")
def order_card():
  if 'identification' in session: 
    if   person['kyc']==True:
        return render_template("/paymentdummy.html",name=person['name'],email=person['email'])
    if   person['kyc']==False or person['kyc']=="":
        return redirect(url_for("welcome"))
  else:
      return redirect(url_for("login"))
@app.route("/paymentwallet")
def order_wallet():
  if 'identification' in session: 
    if   person['kyc']==True:
        return render_template("/paymentwallet.html",name=person['name'],email=person['email'])
    if   person['kyc']==False or person['kyc']=="":
        return redirect(url_for("welcome"))
  else:
      return redirect(url_for("login"))
@app.route("/paymentpl")
def order_pl():
  if 'identification' in session: 
    if   person['kyc']==True:
        return redirect(url_for("/paymentwallet"))
    if   person['kyc']==False or person['kyc']=="":
        return redirect(url_for("welcome"))
  else:
      return redirect(url_for("login"))

#Welcome page
@app.route("/welcome")
def welcome():
    
  if 'identification' in session:
    data = db.child("users").get()
    person["email"] = data.val()[session['identification']]["email"]
    person["contact_id"]=data.val()[session['identification']]["contact_id"]
    person["kyc"]=data.val()[session['identification']]["kyc"]
    if  person["kyc"]==False:
        return render_template("/welcome.html", email = person["email"], name = person["name"])
    if  person["kyc"]==True:
        return render_template("/welcome_after_kyc.html",email=person['email'],name=person['name'])
  else:
      return redirect(url_for("login"))
@app.route("/kyc")
def ky():
    if 'identification' in session and person['kyc']==False:
       return render_template('/kycdummy.html')
    if 'identification' in session and person['kyc']=="":
        return redirect(url_for("welcome"))
    else:
        return redirect(url_for("login"))
@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")
@app.route("/terms&conditions")
def terms_conditions():
    return render_template("terms&conditions.html")
@app.route("/Contactus")
def contactuser():
    return render_template("contact.html")
@app.route("/queryraised",methods=['POST','GET'])
def send_query():
    body=request.form.get("body")
    email=request.form.get("email")
    name=request.form.get("name")
    sendmail('support@cardtobank.net',body,'support request of'+email)
    body1='This mail is to inform you that we have recieved your support request and we will resolve this with in 48 hours'
    sendmail(email,body1,'SUPPORT REQUEST RECIEVED')
    return render_template('contact.html',success='submitted successfully')
# user kyc verification
@app.route("/kycuser",methods=['GET','POST'])
def kyc():
   if 'identification' in session: 
    if (request.method=='POST'):
        pan_number=request.form.get('pan')
        pan_number=pan_number.upper()
        pan_name=request.form.get('panname')
        pan_name=pan_name.upper()
        url='https://pan-card-verification1.p.rapidapi.com/v3/tasks/sync/verify_with_source/ind_pan'
        headers={'Content-Type':'application/json','X-RapidAPI-Host': 'pan-card-verification1.p.rapidapi.com','X-RapidAPI-Key': '17d41157f8msh2de8882d86bab69p1c7f07jsn771b17a881dd'}
        data={"task_id":"74f4c926-250c-43ca-9c53-453e87ceacd1","group_id":"8e16424a-58fc-4ba4-ab20-5bc8e7c3c41e","data":{"id_number":pan_number}}
        data=json.dumps(data)
        response=requests.post(url=url,headers=headers,data=data)
        response1=response.json()
        print(response1)
        if response.status_code==200 and response1['result']['source_output']['name_on_card']==pan_name:
            person['kyc']=True
        
            data={"kyc":True}
            db.child("users").child(person["uid"]).update(data)
            return render_template("/welcome_after_kyc.html",email=person["email"],name=session["name"])
        if response.status_code==200 and response1['result']['source_output']['name_on_card']!=pan_name:
            error='name entered not matched with PAN database'
            return render_template('kycdummy.html',error=error,name=session["name"])
        if response.status_code==200 and response1['result']['source_output']['status']=="id_not_found":
           error="Please enter a valid PAN."
           return render_template('kycdummy.html',error=error,name=session["name"])
        if response.status_code==400 and response1["message"]=="Please enter a valid PAN.":
           error="Please enter a valid PAN."
           return render_template('kycdummy.html',error=error,name=session["name"])
        else:
            error="Something went wrong try again after sometime"
            return render_template('kycdummy.html',error=error,name=session["name"])
   else:
        return redirect(url_for("login"))
# creating order with cashfree
@app.route("/order",methods=['GET','POST'])
def orders():
  if 'identification' in session :
    global person
    if  person['kyc']==True:
        global result
        if request.form.get("UPI ID")=='':
            error='please enter valid upi id'
            return render_template("/paymentdummy.html",error=message,name=person['name'],email=person['email'])
        def amt():
          if(request.method=='POST'):  
            amountinput1=int(request.form.get("amountin"))
            person['amount']=amountinput1
            return amountinput1
        def upi():
            if(request.method=='POST'):
                upiid= str(request.form.get("UPI ID"))
                return upiid
        def get_random_string(length):
           letters = string.ascii_lowercase
           result_str = ''.join(random.choice(letters) for i in range(length))
           result_str="order_"+result_str
       
        DATA1={ "order_id":get_random_string(9) ,
  "order_amount": amt()+amt()*2.5/100,
  "order_currency": "INR",
  "customer_details": {
    "customer_id":"ABC1234" ,
    "customer_email": person["email"],
    "customer_phone": "0000007890"},
  "order_meta":{
      "return_url":"https://a58b-2401-4900-4b54-d8cd-588c-8ec5-3c39-fd66.ngrok.io/complete/{order_id}/{order_token}",
      "payment_method":"cc"}
  }
        body=json.dumps(DATA1)
        headers={'Content-Type': 'application/json','x-api-version': '2022-01-01','x-client-id': key_id,'x-client-secret': secret}
        response=requests.post('https://sandbox.cashfree.com/pg/orders',headers=headers,data=body)
        details1=response.json()
        print(details1)
    
        cf_order_id=details1['order_id']
        cf_token_id=details1['order_token']
        link_for_payment=details1['payment_link']
        person["cashfreeid"]=cf_order_id
        person["cf_token"]=cf_token_id
        return redirect(link_for_payment)
        #if status=='created' and status1=='ERROR':
           # error='please enter valid upi id'
  #return render_template("/paymentdummy.html",error=message,name=person['name'],email=person['email'])
    else:
        return redirect(url_for("welcome"))
  if 'identification' in session and person['kyc']=="":
        return redirect(url_for("welcome")) 
  else:
        return redirect(url_for("login"))
@app.route("/orderwallet",methods=['GET','POST'])
def orders_wallet():
  if 'identification' in session :
    global person
    if  person['kyc']==True:
        global result
        def amt():
          if(request.method=='POST'):  
            amountinput1=int(request.form.get("amountin"))
            person['amount']=amountinput1
            return amountinput1
        def upi():
            if(request.method=='POST'):
                upiid= str(request.form.get("UPI ID"))
                return upiid
        def get_random_string(length):
           letters = string.ascii_lowercase
           result_str = ''.join(random.choice(letters) for i in range(length))
       
        
        DATA1={ "order_id":get_random_string(9) ,
  "order_amount": amt()+amt()*2.5/100,
  "order_currency": "INR",
  "customer_details": {
    "customer_id":"ABC1234" ,
    "customer_email": person["email"],
    "customer_phone": "0000007890"},
  "order_meta":{
      "return_url":"https://a58b-2401-4900-4b54-d8cd-588c-8ec5-3c39-fd66.ngrok.io/complete/{order_id}/{order_token}",
      "payment_method":"app"}
  }
        body=json.dumps(DATA1)
        headers={'Content-Type': 'application/json','x-api-version': '2022-01-01','x-client-id': key_id,'x-client-secret': secret}
        response=requests.post('https://sandbox.cashfree.com/pg/orders',headers=headers,data=body)
        details1=response.json()
        print(details1)
    
        cf_order_id=details1['order_id']
        cf_token_id=details1['order_token']
        link_for_payment=details1['payment_link']
        person["cashfreeid"]=cf_order_id
        person["cf_token"]=cf_token_id
        return redirect(link_for_payment)
        #if status=='created' and status1=='ERROR':
           # error='please enter valid upi id'
  #return render_template("/paymentdummy.html",error=message,name=person['name'],email=person['email'])
    else:
        return redirect(url_for("welcome"))
  if 'identification' in session and person['kyc']=="":
        return redirect(url_for("welcome")) 
  else:
        return redirect(url_for("login"))
#user redirect from cashfree payment page
@app.route('/complete/<path:user_path>',methods=['POST','GET'])
def redirect_user(user_path):
       return redirect("/thankyou") 
#verifying user payment status and transferring money to thier account       
@app.route('/thankyou')
def app_charge():
    global person
    if 'identification' in session and person['kyc']!="" and person['cashfreeid']!="":
        global amount
        url6= "https://sandbox.cashfree.com/pg/orders/"+person['cashfreeid']+"/payments"

        headers = {"Accept": "application/json",'x-client-id':key_id,'x-client-secret':secret,'x-api-version':'2022-01-01'}

        response_of_payment = requests.get(url=url6, headers=headers)
        payment_success_detail=response_of_payment.json()
        person["cashfreeid"]=""
        print(payment_success_detail)
        payment_id = payment_success_detail[0]['cf_payment_id']
        
        payment_message=payment_success_detail[0]['payment_message']  
        payment_status=payment_success_detail[0]['payment_status']  
        DATA4={
            'payment_id':payment_id}
        if payment_status=='SUCCESS':
          DATA3={
                'account_number':'2323230079054709',
                'fund_account_id':person['account_id'],
                'amount':(person['amount']*100),
                'currency':'INR',
                'mode':'UPI',
                'purpose':'payout',
                'currency':'INR',
                }
          url= "https://api.razorpay.com/v1/payments/{}/transfers".format(DATA4['payment_id'])
          url1='https://api.razorpay.com/v1/payouts'
          response_body35=json.dumps(DATA3)
          print(person['account_id'])
          headers={'Content-Type': 'application/json','Authorization':'Basic '+auth_token}
          response1=requests.post(url=url1,headers=headers,data=response_body35)
        
          details3=response1.json()
          print(details3)
          transfer_id=details3['id']
          status_id=details3["status"]
          if status_id=='pending' or status_id=='rejected' or status_id=='queued' or status_id=='cancelled':
              return render_template('payment_failed1.html', order_id=payment_id,reason=payment_message)
          else:
              return render_template("payment_sucess1.html",payment_id=payment_id,payout_id=transfer_id)
        else:
            return render_template('payment_failed1.html', order_id=payment_id,reason=payment_message)
       
      
        
        
        
        with open('payment_success_database.txt', 'a') as p_s_db:
            
            json.dump(payment_success_detail, p_s_db, indent=0)
            
        with open('payment_detail_database.txt', 'a') as p_db:
            
            json.dump(payment_detail, p_db, indent=0)
        return render_template("/thankyou.html", amount = 5000, pay_order_id=pay_order_id,payment_id=payment_id,transfer_id=transfer_id)
    else:
        return redirect(url_for("welcome"))
@app.route("/failed", methods=['POST','GET'])
def failed():
    return render_template('payment_failed1.html', payment_id=payment_id)
@app.route("/sucess")
def sucess():
    return render_template("payment_sucess.html",payment_id=payment_id,payout_id=transfer_id)
#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
            result = request.form           #Get the data
            email = result["email"]
            password = result["pass"]
            try:#Try signing in the user with the given information
                user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
                person["is_logged_in"] = True
                person["email"] = user["email"]
                person["uid"] = user["localId"]
            #Get the name of the user
                data = db.child("users").get()
                person["name"] = data.val()[person["uid"]]["name"]
                person["contact_id"]=data.val()[person["uid"]]["contact_id"]
                person["kyc"]=data.val()[person["uid"]]["kyc"]
                session["name"]=person['name']
                session["identification"]=user["localId"]
            #Redirect to welcome page
                return redirect(url_for('welcome'))
            except:
                error="Invalid email or password"
                return render_template("login.html",error=error)
    else:
        if 'identification' in session :
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

@app.route("/signupuser", methods=["POST","GET"])
def newuser():
    if request.method=="POST":
        global temporary_details
        form=request.form
        name=form["name"]
        email=form["email"]
        password=form["password"]
        number=form["phone"]
        temporary_details['email']=email
        temporary_details['name']=name
        temporary_details['password']=password
        temporary_details['number']=number
        df=pd.read_csv("personal_data.csv")
        if email in df['email'].values:
            error="email already exists"
            return render_template("signup.html",error=error)
        if number in df['phone'].values:
            error="phone number already exists"
            return render_template("signup.html",error=error)
        if email=='' or number=='' or name=='' :
            error='some fields left blank'
            return render_template('signup.html',error=error)
        if len(password)<8 :
            error='password length should be atleast 8'
            return render_template('signup.html',error=error)
        else:
         code=""
         for i in range(0,4):
            code=code+str(randint(0,9))
         print(code)
         temporary_details['code']=code
         body="verification code to register account in C2B :"+code
         temporary_details['body']=body
         sendmail(reciep=email,body=body,subject="VERIFICATION CODE FOR C2B")
         success="otp successfully sent"
         return render_template("validate.html",success=success)
#If someone clicks on register, they are redirected to /register
@app.route("/resend")
def resend():
     global temporary_details
     sendmail(temporary_details['email'],temporary_details['body'],"VERIFICATION CODE FOR C2B")
     success="otp successfully sent"
     return render_template("validate.html",success=success)
 #validating otp and creating user in firebase.   
@app.route("/validateotp", methods = ["POST", "GET"])
def register():
    if request.method == "POST":#Only listen to POST
        global temporary_details
        global person
        result = request.form           #Get the data submitted
        OTP = result["otp"]
        email=temporary_details['email']
        password=temporary_details['password']
        name=temporary_details['name']
        mobile=temporary_details['number']
        if OTP!=temporary_details['code']:
            error='Invalid otp'
            return render_template("validate.html",error=error)
        else:
         try:    #Try creating the user account using the provided data
          auth.create_user_with_email_and_password(email, password)
            #Login the user
          user = auth.sign_in_with_email_and_password(email, password)
          user_data={"email":np.array([email]),"phone":np.array([mobile]),"uid":np.array([user["localId"]])}
          df=pd.DataFrame(data=user_data,columns=['email','phone','uid'])
          print(df)
          df.to_csv('personal_data.csv', mode='a', index=False, header=False)
            #Add data to global person
          DATA={
            'name':name}
          request_body = json.dumps(DATA)
          headers={'Content-Type': 'application/json','Authorization':'Basic '+auth_token}
          response=requests.post('https://api.razorpay.com/v1/contacts',headers=headers,data=request_body)
          details=response.json()
          contact_id=details['id']
         
          person["is_logged_in"] = True
          person["email"] = user["email"]
          person["uid"] = user["localId"]
          person["name"] = name
          person["contact_id"]=contact_id
          person["kyc"]=False
          session["name"]=name
          session["identification"]=user["localId"]
            #Append data to the firebase realtime database
          data = {"name": name, "email": email,"contact_id":contact_id,"kyc":False}
          db.child("users").child(person["uid"]).set(data)
          
            #Go to welcome page
          return redirect(url_for('welcome'))
         except:
            temporary_details={}
            error='something went wrong try again after some time'
            return render_template("validate.html",error=error)
        

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
#@app.before_request
#def before_request():
    #if request.url.startswith('http://'):
        #url = request.url.replace('http://', 'https://', 1)
        #code = 301
        #return redirect(url, code=code)





if __name__== '__main__':
    
    app.run(port=80)
    
                     
