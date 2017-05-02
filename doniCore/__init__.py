from utils import *
from datetime import datetime
import dateutil.parser
from .cache import cache_results


def convert_string_to_utc_time(time_string):
    utc_date = dateutil.parser.parse(time_string)
    return utc_date


def convert_timestamp_to_utc(time_obj):
    date_obj = datetime.strptime('%s%s%s' % (time_obj.tm_mday,
                                             time_obj.tm_mon,
                                             time_obj.tm_year),
                                 '%d%m%Y').date()
    datetime_obj_naive = datetime.strptime(
        date_obj.strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S"
    )
    datetime_obj_utc = datetime_obj_naive.replace(tzinfo=pytz.timezone('UTC'))

    return datetime_obj_utc.strftime("%Y-%m-%d %H:%M:%S %Z%z")

