import time
import urllib.request
import urllib.parse
import re
import telepot

'''Code for a Telegram Bot that takes a statement from the user, and uses it to
 search an audiofile from "myinstants.com", and send it to the user'''

# this variable checks the when the program was turned on, so the bot can work with messages only recieved after this.
timestamp = int(time.time())


def handle(msg):
    if timestamp >= msg['date']:
        return
    force_reply = {'force_reply': True, 'selective': True}
    msg_id = msg['message_id']
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot_name = bot.getMe()['username']
    message = msg['text']
    user_name = msg['from']['first_name']

    print(message)

    if message == '/start' or message == '/help':
        bot.sendMessage(chat_id, "Send me the command /getsound followed by a word or sentence, and find a sound "
                                 "related to it!", reply_to_message_id=msg_id)
        return
    elif message == '/getsound' or message == '/getsound@%s' % bot_name:
        bot.sendMessage(chat_id, "%s, now send me the word or sentence you would like to find a sound" % user_name,
                        reply_to_message_id=msg_id, reply_markup=force_reply)
    elif message.startswith('/getsound'):
        try:
            bot.sendAudio(chat_id, sound_finder(message[10:]), title='Your Sound!', reply_to_message_id=msg_id)
        except AttributeError:
            bot.sendMessage(chat_id, 'Sorry, I could not find any audio related to '
                                     '"%s"' % str(message[10:]), reply_to_message_id=msg_id)
            print('No audio related to %s found' % str(message[10:]))
    try:
        if message[0] != '/' and user_name in msg['reply_to_message']['text']:
            try:
                bot.sendAudio(chat_id, sound_finder(message), title='Your Sound!', reply_to_message_id=msg_id)
            except AttributeError:
                bot.sendMessage(chat_id, 'Sorry, I could not find any audio related to '
                                         '"%s"' % str(message), reply_to_message_id=msg_id)
                print('No audio related to %s found' % message)
    except KeyError:
        pass

# the function used to find the sound itself


def sound_finder(term):
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    term = urllib.parse.quote(term)
    opener = AppURLopener()
    screen1 = (opener.open('https://www.myinstants.com/search/?name=%s' % term)).read()
    m = re.search('/instant/(.+?)/', str(screen1))
    if m:
        key1 = m.group(1)
        screen2 = opener.open('https://www.myinstants.com/instant/%s/' % key1).read()
        m = re.search('href="/media/sounds(.+?)mp3" d', str(screen2))
        if m:
            key2 = m.group(1)
            final_url = 'https://www.myinstants.com/media/sounds/%smp3' % key2
            print('audio link: ', final_url)
            final_file = opener.open(final_url)
            return final_file

token = 'INSERT TOKEN HERE'
bot = telepot.Bot(token)
bot.message_loop(handle)
print('I am listening ...')

while 1:
    time.sleep(10)
