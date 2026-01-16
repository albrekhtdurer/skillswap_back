from datetime import datetime
from dateutil.relativedelta import relativedelta


def conform_years(years: int) -> str:
    """Метод согласования существительного "год" с числительным

    Args:
        years (int): количество лет

    Returns:
        str: строка с нужной формой существительного "год"
    """    
    if years % 10 == 1 and years % 100 != 11:
        return "год"
    elif years % 10 in [2, 3, 4] and years % 100 not in [12, 13, 14]:
        return "года"
    else:
        return "лет"


def prepare_full_user_data(user, skillCanTeach, subcats, images) -> dict:
    """Метод для подготовки данных пользователя для фронтенда (для общего списка пользователей)

    Args:
        user (User): экземпляр класса Пользователя с данными
        skillCanTeach (dict): словарь с данными о навыке, которому может научить пользователь
        subcats (dict): словарь с данными о подкатегориях, навыкам из которых хочет научиться пользователь
        images (dict): словарь с данными о картинках, загруженных пользователем

    Returns:
        dict: словарь с данными пользователя в формате, подходящем для фронтенда
    """    
    user_age = relativedelta(datetime.now(), user.birthDate).years
    user_age_string = str(user_age) + " " + conform_years(user_age)
    result = {
        "id": user.id,
        "name": user.name,
        "location": user.location,
        "likes": user.likes,
        "isLiked": False,
        "age": user_age_string,
        "createdAt": user.createdAt,
        "description": "Пользователь пока не рассказал о себе"
        if user.userDescription == "Напишите пару строк о себе"
        else user.userDescription,
        "avatarUrl": "" if user.avatar == "no avatar" else user.avatar,
        "skillCanTeach": skillCanTeach,
        "subcategoriesWantToLearn": subcats,
        "gender": user.gender,
        "images": [image.path for image in images],
    }

    return result
