import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup


telebot.apihelper.proxy = {'https': 'socks5h://91.221.70.248:9100'}
bot = telebot.TeleBot(config.access_token)

days = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_weekday(web_page, weekday, week):
    soup = BeautifulSoup(web_page, "html5lib")
    index = days.index(weekday) + 1
    # Получаем таблицу с расписанием на понедельник
    if soup.find("table", attrs={"id": str(index) + "day"}) is not None:
        schedule_table = soup.find("table", attrs={"id": str(index) + "day"})

        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        classroom_list = schedule_table.find_all("td", attrs={"class": "room"})
        classroom_list = [room.dd.text for room in classroom_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info])
                        for lesson_info in lessons_list]

    else:
        times_list = locations_list = classroom_list = lessons_list = None
    return times_list, locations_list, classroom_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday',
                               'friday', 'saturday', 'sunday'])
def get_schedule(message, near=False, repeat=0, day=0):
    """ Получить расписание на указанный день """
    if len(message.text.split()) == 2:
        week = (datetime.datetime.today().isocalendar()[1] + 1) % 2 + 1
        weekday, group = message.text.split()
    else:
        weekday, week, group = message.text.split()
    weekday = weekday.replace('/', '')

    if weekday == 'near':
        if datetime.datetime.today().weekday() == 5:
            weekday = 'monday'
            week = (datetime.datetime.today().isocalendar()[1] + 1) % 2
        else:
            weekday = days[datetime.datetime.today().weekday() + repeat]
            week = (datetime.datetime.today().isocalendar()[1] + 1) % 2 + 1

    if weekday == 'tomorrow':
        if datetime.datetime.today().weekday() == 5:
            weekday = 'monday'
            week = (datetime.datetime.today().isocalendar()[1] + 1) % 2
        else:
            weekday = days[datetime.datetime.today().weekday() + 1]
            week = (datetime.datetime.today().isocalendar()[1] + 1) % 2 + 1

    if weekday == 'all':
        weekday = days[day]

    web_page = get_page(group, week)
    times_lst, locations_lst, classroom_lst, lessons_lst = \
        parse_schedule_for_a_weekday(web_page, weekday, week)

    if near:
        if repeat:
            resp = ''
            resp += '<b>{}</b>, {}, {}, {}\n'.format(
                times_lst[0],
                locations_lst[0],
                classroom_lst[0],
                lessons_lst[0])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        else:
            time_now = datetime.datetime.today().time()
            resp = ''
            for ind_time, time in enumerate(times_lst):
                hour, minute = time.split('-')[0].split(':')
                if int(hour) * 60 + int(minute) >= time_now.hour * 60 + \
                        int(minute):
                    resp += '<b>{}</b>, {}, {}, {}\n'.format(
                        times_lst[ind_time],
                        locations_lst[ind_time],
                        classroom_lst[ind_time],
                        lessons_lst[ind_time])
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    return None

            get_schedule(message, near=True, repeat=1)
    else:
        if times_lst is None:
            bot.send_message(message.chat.id, "Выходной!\n")
        else:
            resp = ''
            for time, location, classroom, lession in \
                    zip(times_lst, locations_lst, classroom_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}, {}\n'.format(
                    time, location, classroom, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    week = (datetime.datetime.today().isocalendar()[1] + 1) % 2 + 1
    message.text = message.text.replace(" ", f" {week} ")

    get_schedule(message, near=True)


@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    week = (datetime.datetime.today().isocalendar()[1] + 1) % 2 + 1
    message.text = message.text.replace(" ", f" {week} ")
    get_schedule(message)


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    week = (datetime.datetime.today().isocalendar()[1] + 1) % 2 + 1
    message.text = message.text.replace(" ", f" {week} ")

    for i in range(6):
        try:
            get_schedule(message, day=i)
        except Exception:
            bot.send_message(message.chat.id, "Выходной\n")


if __name__ == '__main__':
    bot.polling(none_stop=True)
