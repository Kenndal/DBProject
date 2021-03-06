import time
from datetime import datetime


class Day:
    def __init__(self, sql_controller, logger, flag=True):
        self.sql_controller = sql_controller
        self.logger = logger
        self.flag = flag
        self.d_id = None
        self.date = None
        self.logger.info("Created instance day.")

    def start(self):
        self.logger.info("Starting counting time in day instance.")
        if self.sql_controller.get_day_date() is None:
            self.get_new_id()
        elif str(datetime.now())[:10] not in self.sql_controller.get_day_date():
            self.get_new_id()
        else:
            self.logger.info("Day with date {} exist in database".format(str(datetime.now())[:10]))

        while True:
            if self.flag:
                if "00:00" in str(time.ctime()):
                    self.get_new_id()
                time.sleep(60)
            else:
                return


    def get_new_id(self):
        temp = self.sql_controller.new_day()
        self.d_id = temp
        self.date = str(datetime.now())[:10]


