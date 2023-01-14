import os
from datetime import datetime

class LogFile:
    __log_index_file_name = 'log_index.txt'
    __log_file_name       = 'log.txt'

    def read_index(self):
        if os.path.exists(self.__log_index_file_name) == True:
            log_file = open(self.__log_index_file_name,'r+')
            lines = log_file.readlines()
        else:
            lines = []
        # print('lines ', lines)
        return lines

    def current_index(self):
        current_index = self.read_index()
        if len(current_index) > 0:
            current_index = int(current_index[0])
        else:
            current_index = 0
        return current_index

    def write_index(self, index):
        log_file = open(self.__log_index_file_name,'w+')
        log_file.write(str(index))

    def read_log(self, index = 0):
        if os.path.exists(self.__log_file_name) == True:
            log_file = open(self.__log_file_name,'r+')
            try:
                lines = log_file.readlines()
            except:
                lines = []
            finally:
                log_file.close()
        else:
            lines = []
        if len(lines) <= 0:
            return ""
        elif index == 0 or index < 0 or index > len(lines):
            return lines[-1]
        else:
            return lines[index]

    def read_last_log(self):
        last_log = self.read_log(0)
        return last_log

    def read_logs(self):
        if os.path.exists(self.__log_file_name) == True:
            log_file = open(self.__log_file_name,'r+')
            lines = log_file.readlines()
        else:
            lines = []
        return lines

    def write_log(self, type, log_string):
        now = datetime.now()
        log_file = open(self.__log_file_name,'a+')
        try:
            log_file.write('[{date}] [{type}] [{text}]\n'.format(date=now, type=type, text=log_string))
        except:
            pass
        finally:
            log_file.close()