from os import name
from random import randint as ri
import db_tools as db
import re
from datetime import datetime

# Add relation between files or folders
class Relation_Utility:

    def __now_timestamp(self):
        # datetime object containing current date and time
        now = datetime.now()
        return str(int(now.timestamp()))

    def __related_ids(self, relations_string):
        regex = r"{source:[\d]+}"
        matches = re.finditer(regex, relations_string, re.MULTILINE)
        found_tags = []
        for matchNum, match in enumerate(matches, start=1):
            g = match.group().replace('(', '').replace(')', '')
            found_tags.append(g)
        return found_tags

    def __get_relations(self, source_id):
        query = 'SELECT `id`, `value` FROM `io_source_meta` where `sourceID` = ' + str(source_id)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__get_relations\")\n", sel[1])
        else:
            if sel[1] > 0:
                relations = sel[2][0][1]
                relations = self.__related_ids(relations)
                for i in range(len(relations)):
                    relations[i] = relations[i].replace('{source:', '')[:-1]
                return relations
                pass
            else:
                return [0]

    def add_relation(self, source_id, related_id):
        if source_id == related_id:
            raise Exception("Error: source and relation must be different.\nYour source and related id is \"" + str(source_id) + "\"")
        relations = self.__get_relations(source_id)
        if relations[0] == 0 and len(relations) == 1:
            query = 'INSERT INTO `io_source_meta` (`sourceID`, `key`, `value`, `createTime`, `modifyTime`) VALUES\
                (' + str(source_id) + ', \'user_sourceAlias\', \'["\{source:' + str(related_id) + '\}/"]\', ' + str(self.__now_timestamp()) + ', ' + str(self.__now_timestamp()) + ')'
            ins = db._insert(query)
            if ins[0] == -1:
                raise Exception("Error on insert to db (\"add_relation\")\n", ins[1])
            else:
                return ins[1]
        elif len(relations) > 0:
            relations_value = ''
            is_related_duplicate = False
            for relation in relations:
                if str(relation) == str(related_id):
                    is_related_duplicate = True
                relations_value += r'"{source:' + str(relation) + '}/",'
            if is_related_duplicate == False:
                relations_value += r'"{source:' + str(related_id) + '}/",'
                relations_value = '[{}]'.format(relations_value[:-1])
                query = 'update `io_source_meta` set value = \'{}\' where `sourceID` = {}'.format(relations_value, source_id)
                upd = db._update(query)
                if upd[0] == -1:
                    raise Exception("Error on update db (\"add_relation\")\n", upd[1])
                else:
                    return upd[1]
        else:
            raise Exception("Error on select from db (\"add_relation\")\n")

    def add_bi_directional_relation(self, first_id, second_id):
        first = self.add_relation(first_id, second_id)
        second = self.add_relation(second_id, first_id)
        return (first, second)


# Create file or folder in kodbox            
class File_and_Folder_Utility:

    def __now_timestamp(self):
        # datetime object containing current date and time
        now = datetime.now()
        return str(int(now.timestamp()))

    def __create_random_list(self, min, max, length):
        randomlist = []
        for i in range(0,length):
            n = ri(min,max)
            randomlist.append(n)
        return randomlist

    def __calc_hash(self):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        random_list = self.__create_random_list(0, len(chars) - 1, 8)
        hash = ''
        for rl in random_list:
            hash += chars[rl]
        query = 'select * from `io_source` where `sourceHash` = "{}"'.format(hash)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__clac_hash\")\n", sel[1])
        else:
            if sel[1] == 0:
                return hash
            else:
                self.__calc_hash()

    def __get_level(self, id): # ./admin/Desktop
        query = 'select `parentLevel` from `io_source` where `sourceID` = {} order by `sourceID` limit 1'.format(id)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__get_level\")\n", sel[1])
        else:
            return sel[2][0][0]

    def __get_id(self, name, is_folder = 1):
        if (is_folder == True) or (is_folder == 1):
            is_folder = 1
        else:
            is_folder = 0
        query = """select `sourceID` from `io_source` where `name` = '{}' and `isFolder` = {}
            order by `sourceID` limit 1""".format(name, is_folder)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__get_id\")\n", sel[1])
        else:
            if sel[1] == 0:
                return -1
            else:
                return sel[2][0][0]

    def __get_parent_id(self, name_id, is_folder = 1):
        if (is_folder == True) or (is_folder == 1):
            is_folder = 1
        else:
            is_folder = 0
        query = """select parentID from io_source where sourceID = {} and isFolder = {}""".format(name_id, is_folder)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__get_parent_id\")\n", sel[1])
        else:
            if sel[1] == 0:
                return -1
            else:
                return sel[2][0][0]

    def __get_name_id(self, name, parent_name, is_folder = 1):
        if (is_folder == True) or (is_folder == 1):
            is_folder = 1
        else:
            is_folder = 0
        query = """select io_source.sourceID from io_source, io_source as parent_source
            where `io_source`.`name` = '{name}' and io_source.parentID = parent_source.sourceID 
            and parent_source.`name` = '{parent_name}'
            and io_source.isFolder = {is_folder}""".format(name=name, parent_name=parent_name, is_folder=is_folder)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__get_name_id\")\n", sel[1])
        else:
            if sel[1] == 0:
                return -1
            else:
                return sel[2][0][0]

    def __get_name_id_with_parent_id(self, name, parent_id, is_folder = 1):
        if (is_folder == True) or (is_folder == 1):
            is_folder = 1
        else:
            is_folder = 0
        query = """select sourceID from io_source where `name` = '{}' and parentID = {} and isFolder = {}""".format(name, parent_id, is_folder)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__get_name_id_with_parent_id\")\n", sel[1])
        else:
            if sel[1] == 0:
                return -1
            else:
                return sel[2][0][0]

    def __create_folder(self, folder_name, parent_name):
        folder_id = self.__get_name_id(folder_name, parent_name, 1)
        if folder_id != -1:
            return folder_id
        parent_id = self.__get_id(parent_name, 1)
        if (parent_id <= 0):
            self.__create_folder(parent_name, 'Desktop')
        parent_id = self.__get_id(parent_name, 1)
        query = '''INSERT INTO `io_source` 
            (`sourceHash`, `targetType`, `targetID`, `createUser`, `modifyUser`, `isFolder`, `name`, `fileType`,
                `parentID`, `parentLevel`, `fileID`, `isDelete`, `size`, `createTime`, `modifyTime`, `viewTime`)
            VALUES ('{}', 1, 1, 1, 1, 1, '{}', '', {}, 
            '{}{},',0, 0, 0, {}, {}, {})'''.format(
                self.__calc_hash(), folder_name, parent_id, 
                self.__get_level(parent_id), self.__get_id(parent_name, 1),
                str(self.__now_timestamp()), str(self.__now_timestamp()), str(self.__now_timestamp()))
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"__create_folder\")\n", ins[1])
        else:
            return ins[1]

    def __create_folder_with_parent_id(self, folder_name, parent_id):
        folder_id = self.__get_name_id_with_parent_id(folder_name, parent_id, 1)
        if folder_id != -1:
            return folder_id
        if (parent_id <= 0):
            raise Exception("Error on select parent folder (\"__create_folder_with_parent_id\")\n")
        query = '''INSERT INTO `io_source` 
            (`sourceHash`, `targetType`, `targetID`, `createUser`, `modifyUser`, `isFolder`, `name`, `fileType`,
                `parentID`, `parentLevel`, `fileID`, `isDelete`, `size`, `createTime`, `modifyTime`, `viewTime`)
            VALUES ('{}', 1, 1, 1, 1, 1, '{}', '', {}, 
            '{}{},',0, 0, 0, {}, {}, {})'''.format(
                self.__calc_hash(), folder_name, parent_id, 
                self.__get_level(parent_id), parent_id,
                str(self.__now_timestamp()), str(self.__now_timestamp()), str(self.__now_timestamp()))
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"__create_folder_with_parent_id\")\n", ins[1])
        else:
            return ins[1]

    def __create_source_event(self, name, is_folder = 1):
        create_type = ''
        if (is_folder == True) or (is_folder == 1):
            is_folder = 1
            create_type = 'mkdir'
        else:
            is_folder = 0
            create_type = 'mkfile'
        name = name.replace("''", "'")
        query = 'select `sourceID`, `parentID` from `io_source` where `name` = "{}" and `isFolder` = {} order by `sourceID` limit 1'.format(name, is_folder)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception('Error on select db\n', sel[1])
        else:
            if sel[1] == 0:
                self.__create_folder(name, 'Desktop')
            else:
                sourceID, parentID = sel[2][0][0], sel[2][0][1]
        name = name.replace("'", "''")
        query_select = 'SELECT id FROM `io_source_event` where sourceID = ' \
            + str(sourceID) + ' and `sourceParent` = ' + str(parentID) + ' '\
        ' and `desc` = \'{\n    "createType": "' + create_type + '",\n    "name": "' + name + '"\n}\''
        sel = db._select(query_select)
        if sel[0] == -1:
            raise Exception('Error on select db\n', sel[1])
        elif sel[1] != 0:
            return sel[2][0][0]

        query = 'INSERT INTO `io_source_event` (`sourceID`, `sourceParent`, `userID`, `type`, `desc`, `createTime`) VALUES'\
        '(' + str(sourceID) + ', ' + str(parentID) + ' '\
        ', 1, \'create\', \'{\n    "createType": "'+ create_type +'",\n    "name": "' + name + '"\n}\', ' + str(self.__now_timestamp()) + ')'
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"__create_source_event\")\n", ins[1])
        else:
            return ins[1]

    def calc_session_id(self):    
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        random_list = self.__create_random_list(0, len(chars) - 1, 32)
        session_id = ''
        for rl in random_list:
            session_id += chars[rl]
        return session_id

    def __create_system_log(self, session_id, source_id, source_parent_id, name, is_folder = 1):
        type = ''
        if (is_folder == True) or (is_folder == 1):
            is_folder = 1
            type = 'mkdir'
        else:
            is_folder = 0
            type = 'mkfile'
        query_find_duplicate = 'SELECT id from `system_log` where '\
        ' `userID` = 1 and `type` = \'file.' + type + '\' and `desc` = \'{"sourceID":' + str(source_id) + ',"sourceParent":"'\
        ' ' + str(source_parent_id) + '","pathName":"' + name + '","pathDisplay":"","userID":"1",'\
        '"type":"create","desc":{"createType":"' + type + '","name":"' + name + '"},'\
        '"sourceTarget":' + str(source_id) + ',"ip":"127.0.0.1"}\''
        sel = db._select(query_find_duplicate)
        # if there is duplicate value, return it's id.
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__count_parent_id\")\n", sel[1])
        elif sel[1] != 0:
                return sel[2][0][0]
        # if there isn't any duplicate value, insert to system log.
        query = 'INSERT INTO `system_log` (`sessionID`, `userID`, `type`, `desc`, `createTime`) VALUES'\
        '(\'' + str(session_id) + '\', 1, \'file.' + type + '\', \'{"sourceID":' + str(source_id) + ',"sourceParent":"'\
        ' ' + str(source_parent_id) + '","pathName":"' + name + '","pathDisplay":"","userID":"1",'\
        '"type":"create","desc":{"createType":"' + type + '","name":"' + name + '"},'\
        '"sourceTarget":' + str(source_id) + ',"ip":"127.0.0.1"}\', ' + str(self.__now_timestamp()) + ')'
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"__create_system_log\")\n", ins[1])
        else:
            return ins[1]

    def __count_parent_id(self, parent_id):
        query = 'select count(*) + 1 from `io_source` where `parentID` = {}'.format(parent_id)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__count_parent_id\")\n", sel[1])
        else:
            if sel[1] == 0:
                return -1
            else:
                return sel[2][0][0]

    def __create_file(self, file_name, parent_name):
        file_id = self.__get_name_id(file_name, parent_name, 0)
        if file_id != -1:
            return file_id
        parent_id = self.__get_id(parent_name, 1)
        if (parent_id <= 0):
            parent_id = self.__create_folder(parent_name, 'Desktop')
        file_type = file_name.split('.')
        file_type = file_type[len(file_type) - 1]
        query = '''INSERT INTO `io_source` 
            (`sourceHash`, `targetType`, `targetID`, `createUser`, `modifyUser`, `isFolder`, `name`, `fileType`,
                `parentID`, `parentLevel`, `fileID`, `isDelete`, `size`, `createTime`, `modifyTime`, `viewTime`)
            VALUES ('{}', 1, 1, 1, 1, 0, '{}', '{}', {}, 
            '{}{},',{}, 0, 0, {}, {}, {})'''.format(
                self.__calc_hash(), file_name, file_type, parent_id, 
                self.__get_level(parent_id), parent_id, self.__count_parent_id(parent_id),
                str(self.__now_timestamp()), str(self.__now_timestamp()), str(self.__now_timestamp()))
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"__create_file\")\n", ins[1])
        else:
            return ins[1]

    def __create_file_with_parent_id(self, file_name, parent_id):
        file_id = self.__get_name_id_with_parent_id(file_name, parent_id, 0)
        if file_id != -1:
            return file_id
        if (parent_id <= 0):
            return -1
        file_type = file_name.split('.')
        file_type = file_type[len(file_type) - 1]
        query = '''INSERT INTO `io_source` 
            (`sourceHash`, `targetType`, `targetID`, `createUser`, `modifyUser`, `isFolder`, `name`, `fileType`,
                `parentID`, `parentLevel`, `fileID`, `isDelete`, `size`, `createTime`, `modifyTime`, `viewTime`)
            VALUES ('{}', 1, 1, 1, 1, 0, '{}', '{}', {}, 
            '{}{},',{}, 0, 0, {}, {}, {})'''.format(
                self.__calc_hash(), file_name, file_type, parent_id, 
                self.__get_level(parent_id), parent_id, self.__count_parent_id(parent_id),
                str(self.__now_timestamp()), str(self.__now_timestamp()), str(self.__now_timestamp()))
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"__create_file\")\n", ins[1])
        else:
            return ins[1]

    def create_folder_on_kodbox(self, folder_name, parent_name, session_id):
        try:
            folder_name = str(folder_name)
            parent_name = str(parent_name)
            folder_name = folder_name.replace("'", "''")
            parent_name = parent_name.replace("'", "''")
            folder_id = self.__create_folder(folder_name, parent_name)
            parent_id = self.__get_parent_id(folder_id, 1)
            self.__create_source_event(folder_name, 1)
            self.__create_system_log(session_id, folder_id, parent_id, folder_name, 1)
            return (folder_id, parent_id)
        except Exception as e:
            raise Exception('When create folder raised below error:\n', e)

    def create_folder_on_kodbox_with_parent_id(self, folder_name, parent_id, session_id):
        try:
            folder_name = str(folder_name)
            folder_name = folder_name.replace("'", "''")
            folder_id = self.__create_folder_with_parent_id(folder_name, parent_id)
            self.__create_source_event(folder_name, 1)
            self.__create_system_log(session_id, folder_id, parent_id, folder_name, 1)
            return (folder_id, parent_id)
        except Exception as e:
            raise Exception('When create folder raised below error:\n', e)

    def create_file_on_kodbox(self, file_name, parent_name, session_id):
        try:
            file_name = str(file_name)
            parent_name = str(parent_name)
            file_name = file_name.replace("'", "''")
            parent_name = parent_name.replace("'", "''")
            file_id = self.__create_file(file_name, parent_name)
            parent_id = self.__get_parent_id(file_id, 0)
            self.__create_source_event(file_name, 0)
            self.__create_system_log(session_id, file_id, parent_id, file_name, 1)
            return (file_id, parent_id)
        except Exception as e:
            raise Exception('When create file raised below error:\n', e) 

    def create_file_on_kodbox_with_parent_id(self, file_name, parent_id, session_id):
        try:
            file_name = str(file_name)
            file_name = file_name.replace("'", "''")

            file_id = self.__create_file_with_parent_id(file_name, parent_id)
            self.__create_source_event(file_name, 0)
            self.__create_system_log(session_id, file_id, parent_id, file_name, 1)
            return (file_id, parent_id)
        except Exception as e:
            raise Exception('When create file raised below error:\n', e)
