import datetime
import os


class Logger:

    LOGFILE = 'log.txt'

    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.filename = os.path.join(basedir, self.LOGFILE)

    def log(self, username, date, ip_address, url):
        date = date if date else datetime.datetime.now()
        with open(self.filename, 'a') as handle:
            handle.write('{0:>10}\t{1}\t{2}\t{3}\n'.format(username, date,
                                                           ip_address, url))

