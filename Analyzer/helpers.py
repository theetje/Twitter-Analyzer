import csv
import numpy
from math import log as log
from datetime import datetime
from collections import OrderedDict

from pprint import pprint

""" get the data from the sql lite database into a dictionary. """
def getPositiveNegativePerDay(session, db_object):
    temp_dict = OrderedDict()

    for positive_words, negative_words, date in session.query(db_object.positive_words, db_object.negative_words, db_object.date):
        str_date = date.strftime('%Y/%m/%d')

        if str_date in temp_dict:
            temp_dict[str_date][0] += positive_words
            temp_dict[str_date][1] += negative_words
        else:
            temp_dict[str_date] = [positive_words, negative_words]

    # Retrun a sorted dict, sorted by key.
    return {k: temp_dict[k] for k in sorted(temp_dict)}

""" Get the delta of the pos - neg ."""
def getXFromData(session, db_object, _Zscore=False):
    result_dict = {}
    prev_day_sentiment = None
    input_dict = getPositiveNegativePerDay(session, db_object)

    for key, value in input_dict.items():
        # Get day sentiment
        result_dict.update({key: value[0] - value[1]})

    mean = numpy.array(list(result_dict.values())).mean(axis=0)
    st_d = numpy.array(list(result_dict.values())).std(axis=0)

    ZXt_dict = {}
    for key, value in result_dict.items():
        ZXt_dict.update({key: ((value - mean)/ st_d)})

    return ZXt_dict

""" Return the Rt value from a CSV. """
def getRFromCSV(start_date, end_date, file_dir, _log=False):
    with open(file_dir) as csvfile:
        reader = csv.DictReader(csvfile)
        _dict = OrderedDict()
        start_date_object = datetime.strptime(start_date, "%Y/%m/%d")
        end_date_object = datetime.strptime(end_date, "%Y/%m/%d")

        # Lees de datum en slot stand in een dict
        for row in reader:
            stock_date_object = datetime.strptime(row['date'], "%x")
            if stock_date_object <= end_date_object and stock_date_object >= start_date_object:
                _dict.update({stock_date_object.strftime('%Y/%m/%d'):float(row['price'].replace(',','.'))})

        # sorteer de dict op datum
        sorted_end_of_day = {k: _dict[k] for k in sorted(_dict)}
        Rt_dict = {}
        prev_value = None

        for key, value in sorted_end_of_day.items():
            if _log:
                if prev_value is not None:
                    if _log:
                        Rt_dict.update({key: log(float(value)) - prev_value})
                prev_value = log(float(value))
            else:
                if prev_value is not None:
                    if _log:
                        Rt_dict.update({key: float(value) - prev_value})
                prev_value = float(value)

        return Rt_dict

""" See if the date match and combine the results if they do."""
def combineRtandXt(Xt_dict, Rt_dict):
    result_array = []
    for Rt_key, Rt_value in Rt_dict.items():
        for Xt_key, Xt_value in Xt_dict.items():

            if Rt_key == Xt_key:
                result_array.extend([[Xt_value,  Rt_value]])

    return result_array



""" Retrun the amount of rows. """
def countRows(session, db_object):
    return session.query(db_object).count()
