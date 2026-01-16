from datetime import datetime


def prepare_current_user_data(user) -> dict:
    """Метод для подготовки данных пользователя для фронтенда (для текущего пользователя)

    Args:
        user (User): экземпляр класса Пользователя с данными

    Returns:
        dict: словарь с данными пользователя в формате, подходящем для фронтенда
    """    
    result = {
        "name": user.name,
        "id": user.id,
        "email": user.email,
        "location": user.location,
        "gender": user.gender,
        "avatarUrl": user.avatar,
        "description": user.userDescription,
        "birthDate": datetime.strftime(user.birthDate, "%Y-%m-%dT%H:%M:%S.%fZ"),
    }

    return result
