
import telebot
from telebot import types
from Osintgram import main
from instagram_private_api.errors import ClientError
import json
from urllib.request import urlretrieve
import os
from seeker import seeker

API = os.getenv("api")
# API = '<BOT-API-TOKEN>'
bot = telebot.TeleBot(API)

BASE_PATH = os.path.dirname(__file__)


def change_target(msg):
    new_uname = msg.json["text"]
    try:
        cmds = main.main(new_uname)
        bot.send_message(msg.chat.id,f"Target changed from {uname} to {new_uname}")
        bot.send_message(msg.chat.id,"Select an option",reply_markup=osintgram_options())
    except ClientError:
        bot.send_message(msg.chat.id,"User not found!")


def osintgram_options():
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(
        types.InlineKeyboardButton(text="Captions",callback_data="captions"),
        types.InlineKeyboardButton(text="Commentdata",callback_data="commentdata"),
        types.InlineKeyboardButton(text="Comments",callback_data="comments"),
        types.InlineKeyboardButton(text="Followers",callback_data="followers"),
        types.InlineKeyboardButton(text="Followings",callback_data="followings"),
        types.InlineKeyboardButton(text="Followers' email",callback_data="fwlersemail"),
        types.InlineKeyboardButton(text="Followings' email",callback_data="fwlingsemail"),
        types.InlineKeyboardButton(text="Followers' number",callback_data="fwlersnum"),
        types.InlineKeyboardButton(text="Followings' number",callback_data="fwlingsnum"),
        types.InlineKeyboardButton(text="hashtags",callback_data="hashtags"),
        types.InlineKeyboardButton(text="Info",callback_data="info"),
        types.InlineKeyboardButton(text="Likes",callback_data="likes"),
        types.InlineKeyboardButton(text="Mediatype",callback_data="mediatype"),
        types.InlineKeyboardButton(text="Photos",callback_data="photos"),
        types.InlineKeyboardButton(text="Profile pic",callback_data="propic"),
        types.InlineKeyboardButton(text="Stories",callback_data="stories"),
        types.InlineKeyboardButton(text="Tagged",callback_data="tagged"),
        types.InlineKeyboardButton(text="People who commented",callback_data="peoplecommented"),
        types.InlineKeyboardButton(text="People who tagged",callback_data="peopletagged"),
        types.InlineKeyboardButton(text="Change Target",callback_data="target")
        )

    return markup

def snd_pics(msg):
    n = msg.json['text']
    ids,counter = cmds['photos'](n=int(n))

    for i in ids:
        filename = os.path.join(os.path.dirname(__file__)+'\\Osintgram\\output\\',f"{uname}_{i}.jpg")
        bot.send_photo(msg.chat.id,open(filename,'rb'))
    bot.send_message(msg.chat.id,"Select an option",reply_markup=osintgram_options())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "captions":
        caps = cmds['captions']()
        if len(caps) > 0:
            for i in caps:
                bot.send_message(call.message.chat.id,f"""{i}""")
        else:
            bot.send_message(call.message.chat.id,"No captions found!!")

        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())
    elif call.data == "commentdata":
        data = cmds['commentdata']()
        if len(data) > 0:
            bot.send_message(call.message.chat.id,"""===================== Comments On Target's Posts ===================== """)
            for i in data:
                bot.send_message(call.message.chat.id,f"""Post-ID:  {i['post_id']}
User-ID:  {i['user_id']}
Username:  {i['username']}
Comment:  {i['comment']}""")
        else:
            bot.send_message(call.message.chat.id,"No comments found on any posts!!")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())
    
    elif call.data == "comments":
        posts,counter = cmds['comments']()
        bot.send_message(call.message.chat.id,f"""Number of posts:  {posts}
Number of comments:  {counter}""")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "followers":
        followers = cmds['followers']()
        if len(followers) > 0:
            bot.send_message(call.message.chat.id,f"""===================== Followers =====================""")
            bot.send_message(call.message.chat.id,f"""Target Total Followers:  {len(followers)}""")

            for follower in followers:
                bot.send_message(call.message.chat.id,f"""ID:  {follower['id']}
Username:  {follower['username']}
Full Name:  {follower['full_name']}""")
        else:
            bot.send_message(call.message.chat.id,"The target doesn't have any followers!")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "followings":
        followings = cmds['followings']()
        if len(followings) > 0:
            bot.send_message(call.message.chat.id,f"""===================== Following =====================""")
            bot.send_message(call.message.chat.id,f"""Target Total Following --> {len(followings)}""")

            for following in followings:
                bot.send_message(call.message.chat.id,f"""ID:  {following['id']}
Username:  {following['username']}
Full Name:  {following['full_name']}""")
        else:
            bot.send_message(call.message.chat.id,"The target is not following anyone!")    
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "fwlersemail":
        bot.send_message(call.message.chat.id,"Searching for emails of followers'...this may take a while")
        fwemails = cmds['fwersemail']()
        if len(fwemails) > 0:    
            bot.send_message(call.message.chat.id,f"""===================== Followers' Email =====================""")
            for i in fwemails:
                bot.send_message(call.message.chat.id,f"""ID:  {i['id']}
Username:  {i['username']}
Full Name:  {i['full_name']}
Email:  {i['email']}""")

        else:
            bot.send_message(call.message.chat.id,"No public emails found!")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "fwlingsemail":
        bot.send_message(call.message.chat.id,"Searching for emails of followings'...this may take a while")
        fwiemails = cmds['fwingsemail']()
        if len(fwiemails) > 0:
            bot.send_message(call.message.chat.id,f"""===================== Followings' Email =====================""")
            for i in fwiemails:
                bot.send_message(call.message.chat.id,f"""ID:  {i['id']}
Username:  {i['username']}
Full Name:  {i['full_name']}
Email:  {i['email']}""")
        else:
            bot.send_message(call.message.chat.id,"No public emails found!") 
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "fwlersnum":
        bot.send_message(call.message.chat.id,"Searching for phone numbers of followers'...this may take a while")
        fwnums = cmds['fwersnumber']()
        print(fwnums)
        if len(fwnums) > 0:
            bot.send_message(call.message.chat.id,f"===================== Catched {len(fwnums)} Numbers =====================")
            for i in fwnums:
                bot.send_message(call.message.chat.id,f"""ID:  {i['id']}
Username:  {i['username']}
Full Name:  {i['full_name']}
Phone:  {i['contact_phone_number']}""")
        else:
            bot.send_message(call.message.id,"Got nothing!!")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "fwlingsnum":
        bot.send_message(call.message.chat.id,"Searching for phone numbers of followings'...this may take a while")
        fwinums = cmds['fwersnumber']()
        if len(fwinums) > 0:
            bot.send_message(call.message.chat.id,f"===================== Catched {len(fwinums)} Numbers =====================")
            for i in fwinums:
                bot.send_message(call.message.chat.id,f"""ID:  {i['id']}
Username:  {i['username']}
Full Name:  {i['full_name']}
Phone:  {i['contact_phone_number']}""")
        else:
            bot.send_message(call.message.id,"Got nothing!!")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "hashtags":
        hashtags = cmds['hashtags']()
        bot.send_message(call.message.chat.id,"===================== Hashtags =====================")
        if hashtags != None:
            for i in hashtags:
                bot.send_message(call.message.chat.id,f"""Hashtag --> {i[0].decode()}
Hashtag Count --> {i[1]}""")
        else:
            bot.send_message(call.message.chat.id,"No hashtags found!!")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "info":
        info = cmds['info']()
        filename = os.path.join(os.path.dirname(__file__)+'\\Osintgram\\output\\',f"{uname}.png")
        urlretrieve(info['profile_pic_url'],filename)

        bot.send_message(call.message.chat.id,f"""===================== User Info =====================""")
        bot.send_photo(call.message.chat.id,open(filename,'rb'),caption=info['username'])
        bot.send_message(call.message.chat.id,f"""User-ID:  {info['pk']}
Username:  {info['username']}
Full Name:  {info['full_name']}
Private Profile:  {info['is_private']}
Media Count:  {info['media_count']}
Follower Count:  {info['follower_count']}
Following Count:  {info['following_count']}
Mutual Followers Count:  {info['mutual_followers_count']}""")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "likes":
        likes,posts = cmds['likes']()
        bot.send_message(call.message.chat.id,f"""Number of Posts:  {posts}
Number of Likes:  {likes}""")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "mediatype":
        total,photo,video = cmds['mediatype']()
        bot.send_message(call.message.chat.id,f"""Total Posts:  {total}
Photos:  {photo}
Videos:  {video}""")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

 
    elif call.data == "photos":
        msg = bot.send_message(call.message.chat.id,"Enter number of posts to be downloaded.")
        bot.register_next_step_handler(msg,snd_pics)

 
    elif call.data == "propic":
        pic = cmds['propic']()  
        filename = os.path.join(os.path.dirname(__file__)+'\\Osintgram\\output\\',f"{uname}.png")
        urlretrieve(pic, filename)
        bot.send_photo(chat_id = call.message.chat.id, photo = open(filename, 'rb'), caption=f"Username:  {uname}")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "stories":
        counter, ids = cmds['stories']()
        for i in ids:
            if i[-1] == 1:
                filename = os.path.join(os.path.dirname(__file__)+'\\Osintgram\\output\\',f"{uname}_{i}w.png")
                bot.send_photo(chat_id = call.message.chat.id, photo = open(filename,'rb'))
            else:
                filename = os.path.join(os.path.dirname(__file__)+'\\Osintgram\\output\\',f"{uname}_{i}.mp4")
                bot.send_video(chat_id = call.message.chat.id, data = open(filename,'rb'), supports_streaming = True)

        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "tagged":
        tag,count = cmds['tagged']()
        if count > 0:
            bot.send_message(call.message.chat.id,f"Total number of people tagged by target --> {count}")
            bot.send_message(call.message.chat.id,"===================== List of tagged users =====================")
            for i in tag:
                bot.send_message(call.message.chat.id,f"""Number of posts --> {i['post']}
Full Name:  {i['full_name']}
Username:  {i['username']}
ID:  {i['id']}""")
        else:
            bot.send_message(call.message.chat.id,"No users tagged by the target!")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "peoplecommented":
        people_commented = cmds['wcommented']()
        if len(people_commented) > 0:
            bot.send_message(call.message.chat.id,"===================== List of users who commented =====================")
            for i in people_commented:
                bot.send_message(call.message.chat.id,f"""ID --> {i['id']}
Username:  {i['username']}
Full Name:  {i['full_name']}
Counter:  {i['counter']}""")
        else:
            bot.send_message(call.message.chat.id,"No users commented!!")
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "peopletagged":
        tagged_by_people = cmds['wtagged']()
        if len(tagged_by_people) > 0:
            bot.send_message(call.message.chat.id,"===================== List of users who tagged the target =====================")
            for i in tagged_by_people:
                bot.send_message(call.message.chat.id,f"""ID --> {i['id']}
Username:  {i['username']}
Full Name:  {i['full_name']}
Counter:  {i['counter']}""")

        else:
            bot.send_message(call.message.chat.id,'The target is tagged by no one!!')
        bot.send_message(call.message.chat.id,"Select an option",reply_markup=osintgram_options())

    elif call.data == "target":
        msg = bot.send_message(call.message.chat.id,'Send new target name.')
        bot.register_next_step_handler(msg,change_target)

    # ------------------------------------------ seeker callback ------------------------------------------    

    elif call.data == 's0':
        bot.answer_callback_query(call.id,"Starting server...")
        SITE = "nearyou"
        global SERVER_PROC
        SERVER_PROC, ngrok_url = seeker.server(SITE,port)
        bot.send_message(call.message.chat.id, f"Send this link to the target: {ngrok_url}")
        bot.send_message(call.message.chat.id, "Waiting for client...")
        try:
            data = seeker.wait()
        except:
            bot.send_message(call.message.chat.id, "Something went wrong!!")
        try:
            bot.send_message(call.message.chat.id, f""" ========= DEVICE INFORMATION ========= 
OS         : {data[-1][0]}
Platform   : {data[-1][1]}
CPU Cores  : {data[-1][2]}
RAM        : {data[-1][3]}
GPU Vendor : {data[-1][4]}
GPU        : {data[-1][5]}
Resolution : {data[-1][6]}
Browser    : {data[-1][7]}
Public IP  : {data[-1][8]}""")

            bot.send_message(call.message.chat.id, f""" ========= IP INFORMATION ========= 
Continent  : {data[-1][9]}
Country    : {data[-1][10]}
Region     : {data[-1][11]}
City       : {data[-1][12]}
Org        : {data[-1][13]}
ISP        : {data[-1][14]}""")

            bot.send_message(call.message.chat.id, f""" ========= LOCATION INFORMATION ========= 
Latitude   : {data[-1][15]}
Longitude  : {data[-1][16]}
Accuracy   : {data[-1][17]}
Altitude   : {data[-1][18]}
Direction  : {data[-1][19]}
Speed      : {data[-1][20]}""")

            bot.send_message(call.message.chat.id, f'Google Maps Link: https://www.google.com/maps/place/{data[-1][15].strip(" deg")}+{data[-1][16].strip(" deg")}')
            seeker.data_parser()

        except:
            bot.send_message(call.message.chat.id,"Error Occured...please try again!!")
            print(f'{seeker.R}[-] {seeker.C}Keyboard Interrupt.{seeker.W}')
            seeker.cl_quit(seeker.SERVER_PROC)

        else:
            seeker.repeat()

    elif call.data == 's1':
        pass

    elif call.data == 's2':
        pass

    elif call.data == 's3':
        pass

    elif call.data == 's4':
        pass

    elif call.data == 's5':
        pass


@bot.message_handler(commands=['start','Start'])
def Main(message):
    bot.send_message(message.chat.id,'Hi there!')
    bot.send_message(message.chat.id, """Commands -
/help
/osintgram
/seeker""")

@bot.message_handler(commands=['osintgram'])
def ask_username(message):
    msg = bot.send_message(message.chat.id, "Send the target Username.")
    bot.register_next_step_handler(msg,osintgram)

def osintgram(message):
    global uname,cmds
    uname = message.json["text"] 
    try:
        cmds = main.main(uname)
        bot.send_message(message.chat.id,"Select an option",reply_markup=osintgram_options())
    except ClientError:
        bot.send_message(message.chat.id,"Something went wrong...please wait for about 5-10 seconds!!")    


# ------------------------------------------ seeker ------------------------------------------
def seeker_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(
        types.InlineKeyboardButton(text="NearYou",callback_data="s0")
        )

    return markup





@bot.message_handler(commands=['seeker'])
def ask_username(message):
    msg = bot.send_message(message.chat.id, "Send Port number")
    bot.register_next_step_handler(msg, start_seeker)

def start_seeker(message):
    global port
    port = int(message.json['text'])
    bot.send_message(message.chat.id, "Select template",reply_markup=seeker_markup())
  
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, """Commands -
/help
/osintgram
/seeker""")
  








bot.infinity_polling()
