# utils/date_utils.py

from datetime import datetime, timedelta
from typing import List

def get_period_days(period: int) -> List[str]:
    """
    Возвращает список дат за определённый период.
    
    :param period: 1 — текущая неделя
    :return: Список дат в формате строки YYYY-MM-DD
    """
    current_date = datetime.now().date()
    weekday = current_date.weekday()

    if period == 1:
        # Текущая неделя (понедельник - воскресенье)
        start_of_week = current_date - timedelta(days=weekday)
        return [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    elif period == 2:
        # Прошлая неделя
        start_of_last_week = current_date - timedelta(days=weekday + 7)
        return [(start_of_last_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    elif period == 3:
        # Месяц
        from calendar import monthrange
        _, days_in_month = monthrange(current_date.year, current_date.month)
        return [(current_date.replace(day=1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days_in_month)]
    else:
        # За всё время
        return []
