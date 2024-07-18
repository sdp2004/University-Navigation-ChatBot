# imporVt cv2
import json
# import json
import os
import random
from chatterbot import ChatBot                                      # chatbot rquired because it contains various function like listtrainer useful in our project of chatbot
from chatterbot.trainers import ListTrainer      
import pyttsx3                    
import speech_recognition
import re
import sys
from tkinter import *
import tkinter as tk
import threading  

from PIL import Image, ImageTk


bot = ChatBot('Bot')                                                # give any name to chatbot, we gave Bot and assigned the variable to it
trainer = ListTrainer(bot)                                          # to train our bot i.e. ek data file di(yml) aur phir run kra phir change kr di data file(.yml) toh purane yml file ka saara content save hoyega ek file mai jisse hume everytime hr data ko load nhi krna padega aur ek baar mai saare files se bot ko train kr do

'''
for files in os.listdir('data/english/'):                           # for files in english directory in data
    data = open('data/english/' + files, 'r', encoding = 'utf-8').readlines()       # encoding utf-8 is for maybe reading or what? | path of file and then + file means file name, readmode, encoding and then read all lines 

    trainer.train(data)                                             # train the data file in db.sqlite3
    
#this is for training the chatbot
'''
data = open('greetings.yml', 'r', encoding = 'utf-8').readlines()
trainer.train(data)




def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully !")
        return json.load(bot_responses)
    
response_data = load_json('bot.json')



def audio_to_text():                                                # we will be using threading here cause if we do not provide thread the compiler will be busy excuting the infinite loop in while True and the rest of the code will not work properly and hence we will use threading where we will asssign one thread to this function and the main thread to execute the rest program so they both work in sync and properly
    while True:                                                     # used this because i want to repeat continous sentences, without it it will run for once and will not work for another sentence 
        sr = speech_recognition.Recognizer()                        # object to recognise the audio
        try:
            with speech_recognition.Microphone()as m:               # m object of microphone 
                sr.adjust_for_ambient_noise(m, duration = 0.1)      # adjust for background disturbance, after 0.2 seconds when we say
                audio = sr.listen(m)                                # listen to audio
                query = sr.recognize_google(audio)                  # converts audio into text
                
                questionField.delete(0, END)                        # delete first at the entry area
                questionField.insert(0, query)                      # then insert query
                botReply()                                          # call function botreply()
                
        except Exception as e:                                      # try aur exception samjha nahi
            print(e)
        

def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        # required_score = 0
        # required_words = response["required_words"]

        # # Check if there are any required words
        # if required_words:
        #     for word in split_message:
        #         if word in required_words:
        #             required_score += 1

        # Amount of required words should match the required score
       #### # if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
                                                        #shift tab below
        for word in split_message:
            # If the word is in the response, add to the score
            if word in response["user_input"]:
                response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    
    max_score_list =  max(score_list)
    insert_index = score_list.index(max_score_list)
    score_list.remove(max_score_list)
    second_max_score_list = max(score_list)
    
    if max_score_list == second_max_score_list:
        bot_answer = bot.get_response(input_string)
        
        if bot_answer != "categories:": 
            return bot_answer
        else:
            return "Please provide a more detailed response"
    
    score_list.insert(insert_index, max_score_list)
    
    best_response = max_score_list
    print(best_response)
    global response_index
    response_index = score_list.index(best_response)

    # Check if input is empty
    if input_string == "":
        return "Please type something so we can chat :("

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]
    
    # if best_response == 0:
    #     bot_answer = bot.get_response(question)
        
    #     if bot_answer != "categories:": 
    #         return bot_answer
    #     else:
    #         return "Please provide a more detailed response"

    # return random.random_string()

def botReply():
    global question
    question = questionField.get()
    question = question.lower()
    # print(question)
    # input=question
    # answer=get_response(question)
    answer = get_response(question)
    print(answer)

        
    textarea.insert(END, "YOU:"+question+"\n\n")
    # textarea.insert(END, "Bot: "+str(answer)+'\n\n')
    textarea.insert(END, "Bot: "+str(answer)+'\n\n')
    pyttsx3.speak(answer)
    questionField.delete(0, END)


root = tk.Tk()

def img_bg1():
    print(question)
    global img
    print(response_data[response_index]["response_type"])
    if(response_data[response_index]["response_type"] == 'library'):
        print("library")
        image=Image.open('./Images/library.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/library.png')
        img=PhotoImage(file= "./Images/library.png")
    elif(response_data[response_index]["response_type"] == 'electronics'):
        print("electronics")
        image=Image.open('./Images/electronics_department.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/electronics_department.png')
        img=PhotoImage(file= "./Images/electronics_department.png")
    elif(response_data[response_index]["response_type"] == 'electrical'):
        print("electrical")
        image=Image.open('./Images/electrical_department.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/electrical_department.png')
        img=PhotoImage(file= "./Images/electrical_department.png")
    elif(response_data[response_index]["response_type"] == 'computer'):
        print("computer")
        image=Image.open('./Images/computer_department.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/computer_department.png')
        img=PhotoImage(file= "./Images/computer_department.png")
    elif(response_data[response_index]["response_type"] == 'administration'):
        print("administration")
        image=Image.open('./Images/administrative.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/administrative.png')
        img=PhotoImage(file= "./Images/administrative.png")
    elif(response_data[response_index]["response_type"] == 'boys hostel'):
        print("boys hostel")
        image=Image.open('./Images/boys_hostel.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/boys_hostel.png')
        img=PhotoImage(file= "./Images/boys_hostel.png")
    elif(response_data[response_index]["response_type"] == 'civil'):
        print("civil")
        image=Image.open('./Images/civil_department.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/civil_department.png')
        img=PhotoImage(file= "./Images/civil_department.png")  
    elif(response_data[response_index]["response_type"] == 'mechanical'):
        print("mechanical")
        image=Image.open('./Images/mechanical_department.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/mechanical_department.png')
        img=PhotoImage(file= "./Images/mechanical_department.png")  
    elif(response_data[response_index]["response_type"] == 'canteen'):
        print("canteen")
        image=Image.open('./Images/canteen.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/canteen.png')
        img=PhotoImage(file= "./Images/canteen.png")  
    elif(response_data[response_index]["response_type"] == 'post office'):
        print("post office")
        image=Image.open('./Images/post_office.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/post_office.png')
        img=PhotoImage(file= "./Images/post_office.png")  
    elif(response_data[response_index]["response_type"] == 'girls hostel'):
        print("girls hostel")
        image=Image.open('./Images/girls_hostel.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/girls_hostel.png')
        img=PhotoImage(file= "./Images/girls_hostel.png")
    elif(response_data[response_index]["response_type"] == 'dispensary'):
        print("dispensary")
        image=Image.open('./Images/dispensary.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/dispensary.png')
        img=PhotoImage(file= "./Images/dispensary.png") 
    elif(response_data[response_index]["response_type"] == 'playground'):
        print("playground")
        image=Image.open('./Images/Playground.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/Playground.png')
        img=PhotoImage(file= "./Images/Playground.png")
    elif(response_data[response_index]["response_type"] == 'shakuntalam'):
        print("shakuntalam ")
        image=Image.open('./Images/shakuntalam.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/shakuntalam.png')
        img=PhotoImage(file= "./Images/shakuntalam.png")
    elif(response_data[response_index]["response_type"] == 'science block'):
        print("science block")
        image=Image.open('./Images/science_block.png')
        new_image = image.resize((800,800)) 
        new_image.save('./Images/science_block.png')
        img=PhotoImage(file= "./Images/science_block.png")
    
    
def newwindow():
    newWindow = Toplevel(root) 
    newWindow.title("Maps of Departments")
    newWindow.geometry("800x800+100+30")
    img_bg1()
    canvas1 = Canvas(newWindow, width = 400,height=400)
    canvas1.pack(fill = "both", expand = True)
    canvas1.create_image( 0, 0, image =img, anchor = "nw")# Display image
    print(question)
    # os.system('python bg.py')
    
thread = threading.Thread(target = audio_to_text)                   # target means which function to put on a seperate thread
thread.daemon = True                                              # when you close the program first this thread will be closed and then the main thread will be closed | without it the thread of the audio_to_text function still keeps on running cause of infinite loop and we need it to stop 
thread.start()    
        

root.geometry('500x570+100+30')
root.title('University Navigation Chatbot')
root.config(bg='red')


image_logo = Image.open('./Images/ymca.png')
resize_image = image_logo.resize((150,150))
logoPic = ImageTk.PhotoImage(resize_image)

logoPicLabel = Label(root, image=logoPic, bg='red')
logoPicLabel.pack(pady=5)

centerFrame = Frame(root)
centerFrame.pack()

scrollbar = Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT)


textarea = Text(centerFrame, font=('times new roman', 20, 'bold'),
                height=10, yscrollcommand=scrollbar.set, wrap='word')
textarea.pack(side=LEFT)
scrollbar.config(command=textarea.yview)


questionField = Entry(root, font=('verdana', 20, 'bold'))
questionField.pack(pady=15, fill=X)

textarea.config()


askPic = PhotoImage(file='./Images/ask.png')
# picPic = PhotoImage(file='./Images/pic.png')

button_frame = Frame(root)
button_frame.pack()

askButton = Button(button_frame, image=askPic, command=botReply)
askButton.pack(side=LEFT)

# direction=Button(button_frame,text="show Command",command=newwindow,height=10)
direction=Button(button_frame,text="show map",command=newwindow, bg='yellow')
direction.pack(side=RIGHT)

def click(event):
    askButton.invoke()
root.bind('<Return>', click)


root.mainloop()