from os import path
from os import mkdir, remove, listdir
from json import dump
from typing import Any, Union
from datetime import datetime as dt

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet


def data_normalizer(data: Any) -> str:
    """
    It takes in any data type and returns a string
    :param data: Any
    :return: A string of the data or datetime string the format of YYYY-MM-DD HH:MM:SS Z
    """
    if isinstance(data, dt):
        return data.strftime("%Y-%m-%d %H:%M:%S %Z")
    return str(data)


def save_file(file_name: str, data: Union[str, list]) -> str:
    """
    It saves a file to a temporary directory
    :param file_name: The name of the file to be saved
    :type file_name: str
    :param data: The data to be saved
    :type data: Union[str, list]
    :return: The path to the file that was created.
    """
    file_path = path.join('administration', 'temp')
    if not path.exists(file_path):
        mkdir(file_path)
    else:
        for file in listdir(file_path):
            remove(path.join(file_path, file))

    with open(path.join(file_path, file_name), 'w') as file:
        if isinstance(data, list):
            dump(data, file, ensure_ascii=False, indent=2, cls=DjangoJSONEncoder)
        else:
            file.write(data)
    return path.join(file_path, file_name)


def to_text(queryset: QuerySet) -> str:
    """
    It takes a queryset and returns the path of text file that was created for it.
    :param queryset: The queryset that you want to convert to a text file
    :type queryset: QuerySet
    :return: The file path of the TEXT file that was created.
    """
    data = queryset.values()
    return save_file(file_name='report.txt', data=list(data))


def to_html(queryset: QuerySet) -> str:
    """
    It takes a queryset, then converts it to a string of html

    :param queryset: The queryset that you want to convert to html
    :type queryset: QuerySet
    :return: the path to the HTML file that was created.
    """
    data = queryset.values()
    html = ''.join('<th>' + data_normalizer(x) + '</th>' for x in data[0].keys())
    for d in data:
        html += '<tr>' + ''.join('<td>' + data_normalizer(x) + '</td>' for x in d.values()) + '</tr>'

    table = '<table border=1 class="dataTable" id="table1", style="margin:auto">' + html + '</table>'
    return save_file(file_name='report.html', data=table)
