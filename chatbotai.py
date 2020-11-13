from newspaper import Article
import random
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings
import datetime
from datetime import datetime
from datetime import date
from newspaper import Article
from nltk.chat.util import Chat, reflections

# Ignore any warning messages
warnings.filterwarnings('ignore')
# Download packages from nltk
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

lista = ['https://sq.wikipedia.org/wiki/Azia', 'https://sq.wikipedia.org/wiki/Evropa']
# vendojme nje url nga ku deshirojme te marrim textin prej ku chatbot do i merr pergjigjet
for list in lista:
    first_article = Article(url="%s" % list)
    first_article.download()
    first_article.parse()
    first_article.nlp()
    corpus = first_article.text

article = Article('https://sq.wikipedia.org/wiki/Koronavirusi')
article.download()
article.parse()
article.nlp()
corpus = article.text

# tokenization, konvertojme tekstin e artikullit ne liste te fjalive
text = corpus
sent_tokens = nltk.sent_tokenize(text)

# largimi i shenjave te pikesimit
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


# krijojme funksion i cili kthen liste te fjaleve te gjitha me shkronja te vogla
def LemNormalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))


root = Tk()
root.overrideredirect(1)
# vendosja e titullit si dhe permasave te dritares
root.title('CHATBOT')
root.geometry('400x500')

img = ImageTk.PhotoImage(Image.open("ai1.png"))
i = Label(image=img)
i.pack()
ttk.Style().configure('TEntry', foreground='orange', bordercolor='black')


def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


# definimi i funksionit per butonin
b = StringVar()


def com():
    today = date.today()
    ora = datetime.now()
    d1 = today.strftime("%d/%m/%Y")
    viti=today.strftime("%Y")
    ora1 = ora.strftime("%H:%M:%S")
    dita = datetime.today().weekday()
    muajii = datetime.now().month

    # shnderrimi i dites nga numer ne string ne gjuhen shqipe
    def week(dita):
        switcher = {
            0: 'Dita e hënë',
            1: 'Dita e martë',
            2: 'Dita e mërkurë',
            3: 'Dita e enjte',
            4: 'Dita e premte',
            5: 'Dita e shtunë',
            6: 'Dita e dielë'
        }
        return switcher.get(dita, "Më falni. Nuk mundem të ju ndihmoj.")

    # shnderrimi i muajit nga numer ne string ne gjuhe shqipe
    def muaji(muajii):
        switcher = {
            1: 'Muaji Janar',
            2: 'Muaji Shkurt',
            3: 'Muaji Mars',
            4: 'Muaji Prill',
            5: 'Muaji Maj',
            6: 'Muaji Qershor',
            7: 'Muaji Korrik',
            8: 'Muaji Gusht',
            9: 'Muaji Shtator',
            10: 'Muaji Tetor',
            11: 'Muaji Nëntor',
            12: 'Muaji Dhjetor'
        }
        return switcher.get(muajii, "Më falni. Nuk mundem të ju ndihmoj.")

    user_response = b.get()
    # definimi i pyetjeve dhe pergjigjeve
    pairs = [
        ['(.*)Unë quhem(.*)|(.*)Unë jam(.*)', ['Përshëndetje %1! Si mundem të ju ndihmoj?']],
        ['Përshëndetje(.*)|Mirëdita(.*)|Mirëmbrema(.*)|Mirëmëngjes(.*)', ['Përshendetje! Si mundem të ju ndihmoj?']],
        ['(.*)Sa vjeç jeni(.*)?|(.*)Sa vjeç je(.*)?', ['Unë jam 10 vjeçar.']],
        ['(.*)Si quheni(.*)?|(.*)Si quhesh(.*)?|(.*)Kush je(.*)?', ['Unë quhem CHATBOT.']],
        ['Kush ju ka krijuar(.*)?|Kush të ka krijuar(.*)?', ['Mua më kanë krijuar Arbi, Ermira dhe Shpëtimi.']],
        ['(.*)Çfarë date jemi sot(.*)?|(.*)Sa është data(.*)?|(.*)Çfarë date është sot(.*)?', [d1]],
        ['(.*)Sa është ora(.*)?', [ora1]],
        ['(.*)Në cilin vit jemi(.*)?', [viti]],
        ['(.*)Çfarë dite është sot(.*)?|(.*)Çfarë dite jemi sot(.*)?', [str(week(dita))]],
        ['(.*)Çfarë muaji është(.*)?|(.*)Në cilin muaj jemi(.*)?|(.*)Cili muaj është(.*)?', [str(muaji(muajii))]]
    ]

    chat = Chat(pairs, reflections)

    chatWindow.insert(INSERT, "\n")
    label1 = Label(chatWindow, text=user_response, font=20, bg='#83B4E7', wraplength=340, justify=LEFT)

    user_response = user_response.lower()

    # pergjigjja e chatbot ne momentin qe pyesim dicka nga url
    robo_response = ''

    # shnderimi i pyetjes tone ne liste te fjalive
    sent_tokens.append(user_response)

    # krijojme TfidfVectorizer Object me qellim qe te konvertojme textin ne matrice
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')

    # konvertojme textin ne matrice
    tfidf = TfidfVec.fit_transform(sent_tokens)

    # pjesa me poshte tregon se si krahasojme te gjita fjalite ne url dhe marrim vleren me te pershtatshme
    vals = cosine_similarity(tfidf[-1], tfidf)

    # marrim indexin e fjalise me te pershtatshme per pyetjen te cilen e kemi bere
    idx = vals.argsort()[0][-2]

    # reduce the dimensionality of vals
    flat = vals.flatten()

    # sort the list in ascending order
    flat.sort()

    # get the most similar score to the users response
    score = flat[-2]

    if (user_response != 'Mire u degjofshim'):
        if (user_response == "Faleminderit(.*)" or user_response == "Ju faleminderit(.*)"):
            label2 = Label(chatWindow, text="Jeni të mirëseardhur!", font=20, bg='#3782CF', wraplength=340,
                           justify=LEFT)
        else:
            if (chat.respond(user_response) != None):
                label2 = Label(chatWindow, text=chat.respond(user_response), font=20, bg='#3782CF', wraplength=340,
                               justify=LEFT)
            elif (score != 0):
                robo_response = robo_response + sent_tokens[idx]
                label2 = Label(chatWindow, text=robo_response, font=20, bg='#3782CF', wraplength=340, justify=LEFT)
            else:
                label2 = Label(chatWindow, text="Më falni. Nuk mundem të ju ndihmoj.", font=20, bg='#3782CF',
                               wraplength=340, justify=LEFT)

        sent_tokens.pop()

    else:
        label2 = Label(chatWindow, text='Mirë u dëgjofshim!', font=20, bg='#3782CF', wraplength=340, justify=LEFT)

    label3 = Label(chatWindow, text="Ti: ", font='Century 12 bold', bg='#83B4E7', wraplength=350, justify=LEFT)
    label4 = Label(chatWindow, text="Chatbot: ", font='Century 12 bold', bg='#3782CF', wraplength=350, justify=LEFT)

    chatWindow.window_create(INSERT, window=label3)
    chatWindow.insert(INSERT, "\n")
    chatWindow.window_create(INSERT, window=label1)
    chatWindow.insert(INSERT, "\n")
    chatWindow.window_create(INSERT, window=label4)
    chatWindow.insert(INSERT, "\n")
    chatWindow.window_create(INSERT, window=label2)
    chatWindow.see("end")
    text.delete(0, END)
    user_response = ''
    robo_response = ''


def clear_search(event):
    text.delete(0, END)
    text.configure(fg='black')


# ndarja e hapsires ne dy pjese (pjesa per input dhe output) si dhe vendosja e scrollbarit
chatWindow = Text(root, bd=1, bg='white', width=50, height=800, )
chatWindow.place(x=30, y=25, height=150, width=509)
scrollbar = Scrollbar(chatWindow)
scrollbar.pack(side=RIGHT, fill=Y)
chatWindow['yscrollcommand'] = scrollbar.set
scrollbar.config(command=chatWindow.yview)

# focus_force is used to take focus
# as soon as application starts


text = Entry(textvariable=b, font=("Century Gothic", 10), width=30, bg='white', fg='#020435')
text.insert(0, 'Klikoni ketu per te komunikuar.')
text.pack()
text.bind("<Button-1>", clear_search)
text.place(x=160, y=345, height=88, width=260)
text.focus_force()
Button1 = Button(text='Send', command=com, bg='black', fg="#37919a", activebackground='#6dffd6', width=12, height=4,
                font=('Century Gothic', 15))
Button1.place(x=225, y=445, height=45, width=120)


def exitt():
    root.destroy()


exitbt = Button(root, text="EXIT", relief=tk.FLAT, bg='white', fg='#020435', activebackground='white', font=("Century Gothic", 10), command=exitt, width=2, height=2)
exitbt.place(x=570, y=175, anchor=tk.SE)

center_window(575, 515)
root.mainloop()
