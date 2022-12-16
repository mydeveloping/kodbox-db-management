from random import randint as ri
import db_tools as db
import re

# Add relation between files or folders
class Relation_Utility:
    def __related_ids(self, book_name):
        regex = r"{source:[\d]+}"
        matches = re.finditer(regex, book_name, re.MULTILINE)
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
        print('relations ', relations)
        if relations[0] == 0 and len(relations) == 1:
            query = 'INSERT INTO `io_source_meta` (`sourceID`, `key`, `value`, `createTime`, `modifyTime`) VALUES\
                (' + str(source_id) + ', \'user_sourceAlias\', \'["\{source:' + str(related_id) + '\}/"]\', 1669968606, 1669968606)'
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

# Create file of folder in kodbox            
class File_and_Folder_Utility:
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
        query = """select `sourceID` from `io_source` where `isFolder` = {} and `name` = '{}'
            order by `sourceID` limit 1""".format(is_folder, name)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__get_id\")\n", sel[1])
        else:
            if sel[1] == 0:
                return -1
            else:
                return sel[2][0][0]

    def __create_folder(self, folder_name, parent_name):
        parent_id = self.__get_id(parent_name, 1)
        if (parent_id <= 0):
            self.__create_folder(parent_name, 'Desktop')
        parent_id = self.__get_id(parent_name, 1)
        query = '''INSERT INTO `io_source` 
            (`sourceHash`, `targetType`, `targetID`, `createUser`, `modifyUser`, `isFolder`, `name`, `fileType`,
                `parentID`, `parentLevel`, `fileID`, `isDelete`, `size`, `createTime`, `modifyTime`, `viewTime`)
            VALUES ('{}', 1, 1, 1, 1, 1, '{}', '', {}, 
            '{}{},',0, 0, 0, 1669968888, 1669968918, 1669968888)'''.format(
                self.__calc_hash(), folder_name, parent_id, 
                self.__get_level(parent_id), self.__get_id(parent_name, 1))
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"__create_folder\")\n", ins[1])
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
        query = 'select `sourceID`, `parentID` from `io_source` where `name` = "{}" and `isFolder` = {} order by `sourceID` limit 1'.format(name, is_folder)
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception('Error on select db\n', sel[1])
        else:
            if sel[1] == 0:
                self.__create_folder(name, 'Desktop')
            else:
                sourceID, parentID = sel[2][0][0], sel[2][0][1]
        query = 'INSERT INTO `io_source_event` (`sourceID`, `sourceParent`, `userID`, `type`, `desc`, `createTime`) VALUES'\
        '(' + str(sourceID) + ', ' + str(parentID) + ' '\
        ', 1, \'create\', \'{\n    "createType": "'+ create_type +'",\n    "name": "' + name + '"\n}\', 1669968888)'
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
        query = 'INSERT INTO `system_log` (`sessionID`, `userID`, `type`, `desc`, `createTime`) VALUES'\
        '(\'' + str(session_id) + '\', 1, \'file.' + type + '\', \'{"sourceID":' + str(source_id) + ',"sourceParent":"'\
        ' ' + str(source_parent_id) + '","pathName":"' + name + '","pathDisplay":"","userID":"1",'\
        '"type":"create","desc":{"createType":"' + type + '","name":"' + name + '"},'\
        '"sourceTarget":' + str(source_id) + ',"ip":"127.0.0.1"}\', 1669968888)'
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
        parent_id = self.__get_id(parent_name, 1)
        if (parent_id <= 0):
            self.__create_folder(parent_name, 'Desktop')
        parent_id = self.__get_id(parent_name, 1)
        file_type = file_name.split('.')
        file_type = file_type[len(file_type) - 1]
        query = '''INSERT INTO `io_source` 
            (`sourceHash`, `targetType`, `targetID`, `createUser`, `modifyUser`, `isFolder`, `name`, `fileType`,
                `parentID`, `parentLevel`, `fileID`, `isDelete`, `size`, `createTime`, `modifyTime`, `viewTime`)
            VALUES ('{}', 1, 1, 1, 1, 0, '{}', '{}', {}, 
            '{}{},',{}, 0, 0, 1669968888, 1669968918, 1669968888)'''.format(
                self.__calc_hash(), file_name, file_type, parent_id, 
                self.__get_level(parent_id), self.__get_id(parent_name, 1), self.__count_parent_id(parent_id))
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"__create_file\")\n", ins[1])
        else:
            return ins[1]

    def create_folder_on_kodbox(self, folder_name, parent_name, session_id):
        try:
            folder_id = self.__create_folder(folder_name, parent_name)
            parent_id = self.__get_id(parent_name, 1)
            self.__create_source_event(folder_name, 1)
            self.__create_system_log(session_id, folder_id, parent_id, folder_name, 1)
            return (folder_id, parent_id)
        except Exception as e:
            raise Exception('When create folder below error raised:\n', e)

    def create_file_on_kodbox(self, file_name, parent_name, session_id):
        try:
            file_id = self.__create_file(file_name, parent_name)
            parent_id = self.__get_id(parent_name, 1)
            self.__create_source_event(file_name, 0)
            self.__create_system_log(session_id, file_id, parent_id, file_name, 1)
            return (file_id, parent_id)
        except Exception as e:
            raise Exception('When create file below error raised:\n', e)