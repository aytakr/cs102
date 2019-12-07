import datetime as dt
from statistics import median
from typing import Optional
import datetime

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    
    s_age = []
    response = get_friends(user_id, 'bdate').json()

    for i in range(len(response['response']['items'])):
        try:
            bdate = response['response']['items'][i]['bdate'].split('.')

            if len(bdate[-1]) == 4:
                age = int(datetime.datetime.now().isocalendar()[0]) - int(bdate[-1])

                s_age.append(age)
        except:
            pass

    return median(s_age)
