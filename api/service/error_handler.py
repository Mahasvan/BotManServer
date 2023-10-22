import inspect
import os
import sys

import db

database = db.Database(os.environ.get("logfile", "log.db"))


def my_except_hook(exctype, value, traceback):
    print("Handler code goes here")
    abspath = inspect.getabsfile(traceback)
    database.error(error=value, file_or_context=abspath)
    sys.__excepthook__(exctype, value, traceback)


def set_exception_handler():
    sys.excepthook = my_except_hook
