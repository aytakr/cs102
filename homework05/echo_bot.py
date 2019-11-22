import telebot
import config

access_token = '997067746:AAHnerSw0RmdgH30eaesq-ZeVg1NIrHgpEE'
telebot.apihelper.proxy = {'https': 'socks5h://194.190.170.38:82'}

bot = telebot.TeleBot(access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling()

config.phone["color"]
