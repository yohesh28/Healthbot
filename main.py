from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
import cv2
import PIL.Image
from PIL import Image
from flask import send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import json
import mysql.connector

#import speech_recognition as sr
#from googletrans import Translator
#from gtts import gTTS

import re
import gensim
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
from gensim.parsing.porter import PorterStemmer
#import spacy
#nlp = spacy.load('en')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="medical_bot"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    msg=""
    mycursor = mydb.cursor()
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cc_register where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('bot')) 
        else:
            msg="You are logged in fail!!!"

    return render_template('index.html',msg=msg)

@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cc_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login_admin.html',msg=msg,act=act)



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    mycursor = mydb.cursor()
    if request.method=='POST':
        file = request.files['file']

        fn="datafile.csv"
        file.save(os.path.join("static/upload", fn))

        filename = 'static/upload/datafile.csv'
        data1 = pd.read_csv(filename, header=0)
        data2 = list(data1.values.flatten())
        '''for ss in data1.values:

            mycursor.execute("SELECT max(id)+1 FROM cc_disease")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            

            sql = "INSERT INTO cc_disease(id,disease,symptom1,symptom2,symptom3,symptom4,symptom5,test1,test2,consultant) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,ss[0],ss[1],ss[2],ss[3],ss[4],ss[5],ss[6],ss[7],ss[8])
            mycursor.execute(sql, val)
            mydb.commit()'''
        
        msg="success"


    return render_template('admin.html',msg=msg)


@app.route('/view_user', methods=['GET', 'POST'])
def view_user():
    value=[]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_register")
    data = mycursor.fetchall()

    
    return render_template('view_user.html', data=data)



@app.route('/register',methods=['POST','GET'])
def register():
    msg=""
    act=""
    mycursor = mydb.cursor()
    name=""
    mobile=""
    mess=""
    uid=""
    if request.method=='POST':
        
        uname=request.form['uname']
        name=request.form['name']     
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']
        pass1=request.form['pass']

        
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM cc_register where uname=%s",(uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM cc_register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            uid=str(maxid)
            sql = "INSERT INTO cc_register(id, name, mobile, email, location,uname, pass,otp,status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
            val = (maxid, name, mobile, email, location, uname, pass1,'','0')
            msg="success"
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
           
        else:
            msg="fail"
            
    return render_template('register.html',msg=msg,mobile=mobile,name=name,mess=mess,uid=uid)

@app.route('/process', methods=['GET', 'POST'])
def process():
    msg=""
    cnt=0
    

    filename = 'static/upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())

    
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt

    
    return render_template('process.html',data=data, msg=msg, rows=rows, cols=cols)

@app.route('/process2', methods=['GET', 'POST'])
def process2():
    msg=""
    act=request.args.get("act")
    
    return render_template('process2.html',msg=msg, act=act)

@app.route('/view_data1', methods=['GET', 'POST'])
def view_data1():
    msg=""
    act=request.args.get("act")
  
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cc_disease")
    data = mycursor.fetchall()   

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from cc_disease where id=%s",(did,))
        mydb.commit()
        msg="ok"
        
    
    return render_template('view_data1.html',msg=msg,act=act,data=data)

@app.route('/add_query', methods=['GET', 'POST'])
def add_query():
    msg=""
    mycursor = mydb.cursor()
    cnt=0
    
    data=[]
    

    mycursor.execute("SELECT * FROM cc_disease")
    data = mycursor.fetchall()
        
    
    if request.method=='POST':
        disease=request.form['disease']
        symptom1=request.form['symptom1']
        symptom2=request.form['symptom2']
        symptom3=request.form['symptom3']
        symptom4=request.form['symptom4']
        symptom5=request.form['symptom5']
        test1=request.form['test1']
        test2=request.form['test2']
        consultant=request.form['consultant']
        mycursor.execute("SELECT max(id)+1 FROM cc_disease")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        

        sql = "INSERT INTO cc_disease(id,disease,symptom1,symptom2,symptom3,symptom4,symptom5,test1,test2,consultant) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,disease,symptom1,symptom2,symptom3,symptom4,symptom5,test1,test2,consultant)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"

    return render_template('add_query.html',msg=msg,data=data)


@app.route('/add_query1', methods=['GET', 'POST'])
def add_query1():
    msg=""
    act=request.args.get("act")
    qid=request.args.get("qid")
    mycursor = mydb.cursor()
    
    cnt=0
    data=[]

    mycursor.execute("SELECT * FROM cc_disease where id=%s",(qid,))
    data = mycursor.fetchone()


    
    if request.method=='POST':
        
        
        disease=request.form['disease']
        symptom1=request.form['symptom1']
        symptom2=request.form['symptom2']
        symptom3=request.form['symptom3']
        symptom4=request.form['symptom4']
        symptom5=request.form['symptom5']
        test1=request.form['test1']
        test2=request.form['test2']
        consultant=request.form['consultant']
        user_query=request.form['user_query']
        
        
        mycursor.execute("update cc_disease set disease=%s,symptom1=%s,symptom2=%s,symptom3=%s,symptom4=%s,symptom5=%s,test1=%s,test2=%s,consultant=%s,user_query=%s where id=%s",(disease,symptom1,symptom2,symptom3,symptom4,symptom5,test1,test2,consultant,user_query,qid))
        mydb.commit()

        msg="success"

    

    return render_template('add_query1.html',msg=msg,qid=qid,act=act,data=data)


@app.route('/view_data2', methods=['GET', 'POST'])
def view_data2():
    msg=""
    mycursor = mydb.cursor()
    cnt=0
    
    data=[]
    

    mycursor.execute("SELECT * FROM cc_location")
    data = mycursor.fetchall()
        
    
    if request.method=='POST':
        hospital=request.form['hospital']
        specialist=request.form['specialist']
        location=request.form['location']
        city=request.form['city']
        treatment=request.form['treatment']
        
       
        mycursor.execute("SELECT max(id)+1 FROM cc_location")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO cc_location(id,hospital,specialist,location,city,treatment,doctor_link) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,hospital,specialist,location,city,treatment,'')
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"

    return render_template('view_data2.html',msg=msg,data=data)


@app.route('/view_data3', methods=['GET', 'POST'])
def view_data3():
    msg=""
    mycursor = mydb.cursor()
    cnt=0
    
    data=[]
    

    mycursor.execute("SELECT * FROM cc_medicine")
    data = mycursor.fetchall()
        
    
    if request.method=='POST':
        medicine=request.form['medicine']
        uses=request.form['uses']
        dosage=request.form['dosage']
        side_effect=request.form['side_effect']
        special=request.form['special']
        
       
        mycursor.execute("SELECT max(id)+1 FROM cc_medicine")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO cc_medicine(id,medicine,uses,dosage,side_effect,special) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (maxid,medicine,uses,dosage,side_effect,special)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"

    return render_template('view_data3.html',msg=msg,data=data)


@app.route('/view_upload', methods=['GET', 'POST'])
def view_upload():
    msg=""
    mycursor = mydb.cursor()
    cnt=0
    filename=""
    data=[]
    

    mycursor.execute("SELECT * FROM cc_image")
    data = mycursor.fetchall()
        
    
    if request.method=='POST':
        disease=request.form['disease']
        img=request.form['img']
        file = request.files['file']
        if file:
            filename=file.filename
            
            file.save(os.path.join("static/data", filename))
        
        
        mycursor.execute("SELECT max(id)+1 FROM cc_image")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO cc_image(id,img_name,disease,img_type) VALUES (%s,%s,%s,%s)"
        val = (maxid,filename,disease,img)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"

    return render_template('view_upload.html',msg=msg,data=data)

            
@app.route('/bot', methods=['GET', 'POST'])
def bot():
    msg=""
    output=""
    uname=""
    mm=""
    mm2=""
    s=""
    fname=""
    xn=0
    if 'username' in session:
        uname = session['username']

    
    
    cnt=0
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      charset="utf8",
      database="medical_bot"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cc_register where uname=%s",(uname, ))
    value = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM cc_data order by rand() limit 0,10")
    data=mycursor.fetchall()
            
    if request.method=='POST':
        msg_input=request.form['msg_input']
        t1=request.form['t1']
        mmc=""
        if msg_input=="hi":
            output="How can i help you?"
        elif msg_input=="":
            output="Sorry, No Results Found!"
        else:
            if t1=="2":
                print("sss")
                
                m1=msg_input.split("\\")
                m3=len(m1)
                print(m3)
                j=0
                for m11 in m1:
                    print(m11)
                    print(j)
                    j+=1

                mm1=m3-1
                mm2=m1[mm1]
                mycursor.execute("SELECT * FROM cc_image where img_name like %s",(mm2,))
                dd44=mycursor.fetchall()
                for dd45 in dd44:
                    mmc=dd45[3]
            #nlp=STOPWORDS
            #def remove_stopwords(text):
            #    clean_text=' '.join([word for word in text.split() if word not in nlp])
            #    return clean_text
            ##
            #txt=remove_stopwords(msg_input)
            ##
            #print("img")
            #print(mm2)
            stemmer = PorterStemmer()
        
            from wordcloud import STOPWORDS
            STOPWORDS.update(['rt', 'mkr', 'didn', 'bc', 'n', 'm', 
                              'im', 'll', 'y', 've', 'u', 'ur', 'don', 
                              'p', 't', 's', 'aren', 'kp', 'o', 'kat', 
                              'de', 're', 'amp', 'will'])

            def lower(text):
                return text.lower()

            def remove_specChar(text):
                return re.sub("#[A-Za-z0-9_]+", ' ', text)

            def remove_link(text):
                return re.sub('@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+', ' ', text)

            def remove_stopwords(text):
                return " ".join([word for word in 
                                 str(text).split() if word not in STOPWORDS])

            def stemming(text):
                return " ".join([stemmer.stem(word) for word in text.split()])

            #def lemmatizer_words(text):
            #    return " ".join([lematizer.lemmatize(word) for word in text.split()])

            def cleanTxt(text):
                text = lower(text)
                text = remove_specChar(text)
                text = remove_link(text)
                text = remove_stopwords(text)
                text = stemming(text)
                
                return text

            
            if t1=="2":
                mm='%'+mmc+'%'
            else:
                clean_msg=cleanTxt(msg_input)
                print(clean_msg)
                mm='%'+msg_input+'%'
            
            dm=""
            mycursor.execute("SELECT count(*) FROM cc_disease where disease like %s || user_query like %s || symptom1 like %s || symptom2 like %s || consultant like %s",(mm,mm,mm,mm,mm))
            cnt1=mycursor.fetchone()[0]
            if cnt1>0:
                
                mycursor.execute("SELECT * FROM cc_disease where disease like %s || user_query like %s || symptom1 like %s || symptom2 like %s || consultant like %s",(mm,mm,mm,mm,mm))
                dd=mycursor.fetchall()
                for dd1 in dd:
                    dm+="<h5>Disease: "+dd1[1]+"</h5><br>"
                    dm+="Symptom1: "+dd1[2]+"<br>"
                    dm+="Symptom2: "+dd1[3]+"<br>"
                    dm+="Symptom3: "+dd1[4]+"<br>"
                    dm+="Symptom4: "+dd1[5]+"<br>"
                    dm+="Symptom5: "+dd1[6]+"<br>"
                    dm+="Test1: "+dd1[7]+"<br>"
                    dm+="Test2: "+dd1[8]+"<br>"
                    dm+="Consultant: "+dd1[9]+"<br><br>"
                    

            mycursor.execute("SELECT count(*) FROM cc_location where hospital like %s || specialist like %s || city like %s || treatment like %s || user_query like %s",(mm,mm,mm,mm,mm))
            cnt2=mycursor.fetchone()[0]
            if cnt2>0:
                
                mycursor.execute("SELECT * FROM cc_location where hospital like %s || specialist like %s || city like %s || treatment like %s || user_query like %s",(mm,mm,mm,mm,mm))
                dd2=mycursor.fetchall()
                for dd21 in dd2:
                    dm+="<br><h5>Hospital: "+dd21[1]+"</h5>"
                    dm+="Specialist: "+dd21[2]+"<br>"
                    dm+="Location: "+dd21[3]+"<br>"
                    dm+="City: "+dd21[4]+"<br>"
                    dm+="Treatment: "+dd21[5]+"<br>"
                    dm+="Video Conference: <a href=http://localhost:5000/meet?doctor="+dd21[2]+" target=_blank>Click</a><br>"
                   
            mycursor.execute("SELECT count(*) FROM cc_medicine where medicine like %s || user_query like %s",(mm,mm))
            cnt3=mycursor.fetchone()[0]
            if cnt3>0:
                mycursor.execute("SELECT * FROM cc_medicine where medicine like %s || user_query like %s",(mm,mm))
                dd3=mycursor.fetchall()
                for dd31 in dd3:
                    dm+="<br><h5>Medicine: "+dd31[1]+"</h5>"
                    dm+="Uses: "+dd31[2]+"<br>"
                    dm+="Dosage: "+dd31[3]+"<br>"
                    dm+="Side Effect: "+dd31[4]+"<br>"
                    dm+="Special Consideration: "+dd31[5]+"<br>"

            mmg=""
            if t1=="2":
                m1=msg_input.split("\\")
                m3=len(m1)
                mm1=m3-1
                mm2=m1[mm1]
                mmg=mm2
            mycursor.execute("SELECT count(*) FROM cc_image where img_name like %s || disease like %s",(mmg,mm))
            cnt4=mycursor.fetchone()[0]
            if cnt4>0:
                mycursor.execute("SELECT * FROM cc_image where img_name like %s || disease like %s",(mmg,mm))
                dd4=mycursor.fetchall()
                for dd41 in dd4:
                    
                    dm+="<img src=../static/data/"+dd41[1]+" width=150 height=150><br>"
                    dm+=""+dd41[2]+"<br><br>"

            mycursor.execute("SELECT count(*) FROM cc_data where user_query like %s",(mm,))
            cnt5=mycursor.fetchone()[0]
            if cnt5>0:
                mycursor.execute("SELECT * FROM cc_data where user_query like %s",(mm,))
                dd5=mycursor.fetchall()
                for dd51 in dd5:
                    dm+="<br>"+dd51[2]+"</h5>"
                    dm+=""+dd51[3]+"<br>"

            
            if cnt1>0 or cnt2>0 or cnt3>0 or cnt4>0 or cnt5>0:
                output=dm


                
                '''result=""
                ###########
                lg=request.form['language']
                if lg=="":
                    output=dm
                else:
                    translator = Translator()
                    
                    #recognized_text=request.form['message']
                    recognized_text=dm
                    
                        
                    if recognized_text:
                        #try:
                        available_languages = {
                            'ta': 'Tamil',
                            'hi': 'Hindi',
                            'ml': 'Malayalam',
                            'kn': 'Kannada',
                            'te': 'Telugu',
                            'mr': 'Marathi',
                            'ur': 'Urdu',
                            'bn': 'Bengali',
                            'gu': 'Gujarati',
                            'fr': 'French'
                        }

                        print("Available languages:")
                        for code, language in available_languages.items():
                            print(f"{code}: {language}")

                        #selected_languages = input("Enter the language codes (comma-separated) you want to translate to: ").split(',')
                        selected_languages=lg.split(',')
                       
                        if not os.path.exists("static/translations"):
                            os.makedirs("static/translations")

                       
                        for lang_code in selected_languages:
                            lang_code = lang_code.strip()
                            if lang_code in available_languages:
                                translated = translator.translate(recognized_text, dest=lang_code)
                                print(f"Translation in {available_languages[lang_code]} ({lang_code}): {translated.text}")

                                
                                text_filename = f"static/translations/translation_{lang_code}.txt"
                                with open(text_filename, "w", encoding="utf-8") as text_file:
                                    text_file.write(f"Translation in {available_languages[lang_code]} ({lang_code}):\n{translated.text}")
                                print(f"Translation saved as '{text_filename}'")
                                #text_files.append(text_filename)
                                result=translated.text
                                print(result)
                        #except Exception as e:
                        #    result=dm
                        #    print("An error occurred during translation:", e)                    
                    ##############
                    #ff=open("static/translations/translation_ta.txt","r")
                    #resu=ff.read()
                    #ff.close()
                    output=result'''

            else:
                if msg_input=="":
                    output="How can i help you?"
                elif msg_input=="hi":
                    output="How can i help you?"
                else:
                    output="Sorry, No Results Found!"


            '''else:
                mm='%'+mm2+'%'
                
                mycursor.execute("SELECT count(*) FROM cc_data where input=%s",(mm2,))
                cnt=mycursor.fetchone()[0]
                if cnt>0:
                    dss=""
                    mycursor.execute("SELECT * FROM cc_data where input=%s",(mm2,))
                    dd=mycursor.fetchall()
                    for dd1 in dd:
                        print(dd1[1])
                        dss="<img src=../static/data/"+dd1[1]+" width=150 height=150><br><br>"
                        dss+=dd1[2]
                    output=dss

                else:
                    if msg_input=="":
                        output="How can i help you?"
                    elif msg_input=="hi":
                        output="How can i help you?"
                    else:
                        output="Sorry, No Results Found!"'''
                

        return json.dumps(output)


    return render_template('bot.html', msg=msg,output=output,uname=uname,data=data,value=value)   

#LSTM-Classification
class LSTM():
    INPUT_VECTOR_LENGTH = 20
    OUTPUT_VECTORLENGTH = 20
    minimum_length = 2
    maximum_length = 20
    sample_size = 30000 
    WORD_START = 1
    WORD_PADDING = 0

    def extract_converstionIDs(conversation_lines):
        conversations = []
        for line in conversation_lines[:-1]:
            split_line = line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
            conversations.append(split_line.split(','))
        return conversations

    def extract_quesans_pairs(linetoID_mapping,conversations):
        questions = []
        answers = []
        for con in conversations:
            for i in range(len(con)-1):
                questions.append(linetoID_mapping[con[i]])
                answers.append(linetoID_mapping[con[i+1]])
        return questions,answers
    def transform_text(input_text):
        input_text = input_text.lower()
        input_text = re.sub(r"I'm", "I am", input_text)
        input_text = re.sub(r"he's", "he is", input_text)
        input_text = re.sub(r"she's", "she is", input_text)
        input_text = re.sub(r"it's", "it is", input_text)
        input_text = re.sub(r"that's", "that is", input_text)
        input_text = re.sub(r"what's", "that is", input_text)
        input_text = re.sub(r"where's", "where is", input_text)
        input_text = re.sub(r"how's", "how is", input_text)
        input_text = re.sub(r"\'ll", " will", input_text)
        input_text = re.sub(r"\'ve", " have", input_text)
        input_text = re.sub(r"\'re", " are", input_text)
        input_text = re.sub(r"\'d", " would", input_text)
        input_text = re.sub(r"\'re", " are", input_text)
        input_text = re.sub(r"won't", "will not", input_text)
        input_text = re.sub(r"can't", "cannot", input_text)
        input_text = re.sub(r"n't", " not", input_text)
        input_text = re.sub(r"'til", "until", input_text)
        input_text = re.sub(r"[-()\"#/@;:<>{}`+=~|]", "", input_text)
        input_text = " ".join(input_text.split())
        return input_text

    def filter_ques_ans(clean_questions,clean_answers):
        # Filter out the questions that are too short/long
        short_questions_temp = []
        short_answers_temp = []
        for i, question in enumerate(clean_questions):
            if len(question.split()) >= minimum_length and len(question.split()) <= maximum_length:
                short_questions_temp.append(question)
                short_answers_temp.append(clean_answers[i])
        short_questions = []
        short_answers = []
        for i, answer in enumerate(short_answers_temp):
            if len(answer.split()) >= minimum_length and len(answer.split()) <= maximum_length:
                short_answers.append(answer)
                short_questions.append(short_questions_temp[i])
        return short_questions,short_answers

    def create_vocabulary(tokenized_ques,tokenized_ans):
        vocabulary = {}
        for question in tokenized_ques:
            for word in question:
                if word not in vocabulary:
                    vocabulary[word] = 1
                else:
                    vocabulary[word] += 1
        for answer in tokenized_ans:
            for word in answer:
                if word not in vocabulary:
                    vocabulary[word] = 1
                else:
                    vocabulary[word] += 1  
        return vocabulary

    def create_encoding_decoding(vocabulary):
        threshold = 15
        count = 0
        for k,v in vocabulary.items():
            if v >= threshold:
                count += 1
        vocab_size  = 2 
        encoding = {}
        decoding = {1: 'START'}
        for word, count in vocabulary.items():
            if count >= threshold:
                encoding[word] = vocab_size 
                decoding[vocab_size ] = word
                vocab_size += 1
        return encoding,decoding,vocab_size
    def transform(encoding, data, vector_size=20):
        transformed_data = np.zeros(shape=(len(data), vector_size))
        for i in range(len(data)):
            for j in range(min(len(data[i]), vector_size)):
                try:
                    transformed_data[i][j] = encoding[data[i][j]]
                except:
                    transformed_data[i][j] = encoding['<UNKNOWN>']
        return transformed_data
    def create_gloveEmbeddings(encoding,size):
        file = open(GLOVE_MODEL, mode='rt', encoding='utf8')
        words = set()
        word_to_vec_map = {}
        for line in file:
            line = line.strip().split()
            word = line[0]
            words.add(word)
            word_to_vec_map[word] = np.array(line[1:], dtype=np.float64)
        embedding_matrix = np.zeros((size, 50))
        for word,index in encoding.items():
            try:
                embedding_matrix[index, :] = word_to_vec_map[word.lower()]
            except: continue
        return embedding_matrix

    def create_model(dict_size,embed_layer,hidden_dim):
    
        encoder_inputs = Input(shape=(maximum_length, ), dtype='int32',)
        encoder_embedding = embed_layer(encoder_inputs)
        encoder_LSTM = LSTM(hidden_dim, return_state=True)
        encoder_outputs, state_h, state_c = encoder_LSTM(encoder_embedding)
        decoder_inputs = Input(shape=(maximum_length, ), dtype='int32',)
        decoder_embedding = embed_layer(decoder_inputs)
        decoder_LSTM = LSTM(hidden_dim, return_state=True, return_sequences=True)
        decoder_outputs, _, _ = decoder_LSTM(decoder_embedding, initial_state=[state_h, state_c])
        outputs = TimeDistributed(Dense(dict_size, activation='softmax'))(decoder_outputs)
        model = Model([encoder_inputs, decoder_inputs], outputs)
        return model

    def prediction_answer(user_input,model):
        transformed_input = transform_text(user_input)
        input_tokens = [nltk.word_tokenize(transformed_input)]
        input_tokens = [input_tokens[0][::-1]]  #reverseing input seq
        encoder_input = transform(encoding, input_tokens, 20)
        decoder_input = np.zeros(shape=(len(encoder_input), OUTPUT_VECTORLENGTH))
        decoder_input[:,0] = WORD_START
        for i in range(1, OUTPUT_VECTORLENGTH):
            pred_output = model.predict([encoder_input, decoder_input]).argmax(axis=2)
            decoder_input[:,i] = pred_output[:,i]
        return pred_output

##########################

    
@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];

    print(password)
    return json.dumps({'status':'OK','user':user,'pass':password});


@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=request.args.get("msg")
    act=request.args.get("act")
    url=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cc_data")
    data = mycursor.fetchall()   

    if request.method=='POST':
        user_query=request.form['user_query']
        response1=request.form['response1']
        response2=request.form['response2']

        '''if link is None:
            url=""
        else:
            #url=' <a href='+link+' target="_blank">Click Here</a>'
            url=""
        output+=url'''
        
        mycursor.execute("SELECT max(id)+1 FROM cc_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO cc_data(id,user_query,response1,response2) VALUES (%s,%s,%s,%s)"
        val = (maxid,user_query,response1,response2)
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Added Success")
        
        return redirect(url_for('view_data',msg='success'))
        #if cursor.rowcount==1:
        #    return redirect(url_for('index',act='1'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from cc_data where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_data'))
    
    
    return render_template('view_data.html',msg=msg,act=act,data=data)


@app.route('/edit2', methods=['GET', 'POST'])
def edit2():
    msg=request.args.get("msg")
    act=request.args.get("act")
    eid=request.args.get("qid")
    url=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cc_location where id=%s",(eid,))
    data1 = mycursor.fetchall()
    
    mycursor.execute("SELECT * FROM cc_location where id=%s",(eid,))
    data = mycursor.fetchone()
    

    if request.method=='POST':
        hospital=request.form['hospital']
        specialist=request.form['specialist']
        location=request.form['location']
        city=request.form['city']
        treatment=request.form['treatment']
        
        user_query=request.form['user_query']

        mycursor.execute("update cc_location set hospital=%s,specialist=%s,location=%s,city=%s,treatment=%s,user_query=%s where id=%s",(hospital,specialist,location,city,treatment,user_query,eid))
        mydb.commit()
        msg="success"

    return render_template('edit2.html',msg=msg,act=act,data=data,data1=data1)

@app.route('/edit3', methods=['GET', 'POST'])
def edit3():
    msg=request.args.get("msg")
    act=request.args.get("act")
    eid=request.args.get("eid")
    url=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cc_medicine where id=%s",(eid,))
    data1 = mycursor.fetchall()
    
    mycursor.execute("SELECT * FROM cc_medicine where id=%s",(eid,))
    data = mycursor.fetchone() 

    if request.method=='POST':
        medicine=request.form['medicine']
        uses=request.form['uses']
        dosage=request.form['dosage']
        side_effect=request.form['side_effect']
        special=request.form['special']
        user_query=request.form['user_query']

        mycursor.execute("update cc_medicine set medicine=%s,uses=%s,dosage=%s,side_effect=%s,special=%s,user_query=%s where id=%s",(medicine,uses,dosage,side_effect,special,user_query,eid))
        mydb.commit()
        msg="success"

    return render_template('edit3.html',msg=msg,act=act,data=data,data1=data1)

@app.route('/meet', methods=['GET', 'POST'])
def meet():
    msg=""
    doctor=request.args.get("doctor")

    return render_template('meet.html',msg=msg,doctor=doctor)

@app.route('/meetapi',methods=['POST','GET'])
def meetapi():
    msg=""

    return render_template('meetapi.html',msg=msg)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    msg=request.args.get("msg")
    act=request.args.get("act")
    eid=request.args.get("eid")
    url=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cc_data")
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM cc_data where id=%s",(eid,))
    data2 = mycursor.fetchone() 

    if request.method=='POST':
        user_query=request.form['user_query']
        response1=request.form['response1']
        response2=request.form['response2']


        mycursor.execute("update cc_data set user_query=%s,response1=%s,response2=%s where id=%s",(user_query,response1,response2,eid))
        mydb.commit()

        
        print(mycursor.rowcount, "Added Success")
        
        return redirect(url_for('view_data',msg='success'))
        #if cursor.rowcount==1:
        #    return redirect(url_for('index',act='1'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from cc_data where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_data'))
    
    
    return render_template('edit.html',msg=msg,act=act,data=data,data2=data2)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    msg=request.args.get("msg")
    act=request.args.get("act")
    url=""
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cc_data")
    data = mycursor.fetchall()   

    if request.method=='POST':
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            
            file.save(os.path.join("static/upload", filename))

            ff = 'static/upload/'+filename
            data1 = pd.read_csv(ff, header=0)
            for ss in data1.values:
                mycursor.execute("SELECT max(id)+1 FROM cc_data")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                
                uid=str(maxid)
                sql = "INSERT INTO cc_data(id,input,output) VALUES (%s, %s, %s)"
                val = (maxid, ss[0],ss[1])
                msg="success"
                mycursor.execute(sql, val)
                mydb.commit()      
            
        return redirect(url_for('view_data'))
    
    
    return render_template('upload.html',msg=msg,act=act,data=data)

@app.route('/down', methods=['GET', 'POST'])
def down():
    fn = request.args.get('fname')
    path="static/upload/"+fn
    return send_file(path, as_attachment=True)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
