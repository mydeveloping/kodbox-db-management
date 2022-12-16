import db_tools as db
import json

class Tag_Utility:
    __TAG_PREFIX = 'label'
    __TAG_NAME = ["grey", "red", "orange", "yellow", "green", "cyan", "blue","purple","pink"]
    __TAG_COLOR_TYPE = ['light', 'normal', 'deep']

    def __init__(self):
        self.TAG_COLORS = []

    def __tag_colors(self):
        tc = []
        for tn in self.__TAG_NAME:
            for tct in self.__TAG_COLOR_TYPE:
                tc.append('{}-{}-{}'.format(self.__TAG_PREFIX, tn, tct))
        self.TAG_COLORS = tc

    def __get_max_tag_id(self):
        query = 'SELECT `id`, `value` + 1 as newKey FROM `user_option` where `key` = \'MAX-ID\' and `type` = \'User.tagList-ID\''
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"__get_max_tag_id\")\n", sel[1])
        else:
            if sel[1] == 0:
                raise Exception("Error on select from `user_option`: 'MAX-ID' not found in 'key' field.")
            else:
                return (int(sel[2][0][0]), int(sel[2][0][1])) # id, newKey

    def get_tag_list(self):
        query = "SELECT `value` FROM `user_option` WHERE `type` = 'User.tagList' AND `key` LIKE 'ID-%'"
        sel = db._select(query)
        if sel[0] == -1:
            raise Exception("Error on select from db (\"get_tag_list\")\n", sel[1])
        else:
            tags = sel[2]
            tag_list = []
            for t in tags:
                data = json.loads(t[0])
                tag_list.append(data["name"])
            return tag_list

    def is_tag_name_exist(self, tag_name):
        tag_list = self.get_tag_list()
        return tag_name in tag_list

    def create_tag(self, tag_name, tag_color = 'label-blue-normal'):
        if self.is_tag_name_exist(tag_name):
            """SELECT `id`, cast(SUBSTR(`key`, 4, 10) as UNSIGNED) as tag_id FROM `user_option` WHERE `type` = 'User.tagList' AND `key` LIKE 'ID-%' and `value` LIKE '%"name": "Ahmad-Tag",%'"""
            query = '''SELECT cast(SUBSTR(`key`, 4, 10) as UNSIGNED) as tag_id, `id` FROM `user_option` 
                WHERE `type` = 'User.tagList' AND `key` LIKE 'ID-%' and `value` LIKE '%"name": "{}",%' '''.format(tag_name)
            sel = db._select(query)
            if sel[0] == -1:
                raise Exception("Error on select from db (\"get_tag_list\")\n", sel[1])
            else:
                return sel[2][0][0]
        if tag_color[:6] != 'label-':
            tag_color = 'label-' + tag_color
        if tag_color not in self.TAG_COLORS:
            tag_color = 'label-blue-normal'
        tag_id = self.__get_max_tag_id()
        query_add_tag = 'INSERT INTO `user_option` (`userID`, `type`, `key`, `value`, `createTime`, `modifyTime`) VALUES' \
            + '     (1, \'User.tagList\', \'ID-' + str(tag_id[1]) \
            + '\', \'{\n    "name": "' + tag_name \
            + '",\n    "style": "' + tag_color + '",\n    "sort": ' + str(tag_id[1]) + ',\n    "id": ' + str(tag_id[1]) + ',\n    "createTime": 1669969776,\n    "modifyTime": 1669969776\n}\' '\
            +', 1669969776, 1669969776);'   
        ins = db._insert(query_add_tag)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"create_tag\")\n", ins[1])
        else:
            query_update_tagListID = '''UPDATE `kodbox`.`user_option` SET `value` = {} where id = {}'''.format(tag_id[1], tag_id[0])
            upd = db._update(query_update_tagListID)
            if upd[0] == -1:
                raise Exception("Error on update db (\"add_relation\")\n", upd[1])
            else:
                return tag_id[1]

    def add_tag_to_file_or_folder(self, file_or_folder_id, tag_id):
        query = '''INSERT INTO `user_fav` (`userID`, `tagID`, `name`, `path`, `type`, `sort`, `modifyTime`, `createTime`) VALUES
        (1, {}, '', '{}', 'source', 0, 1670798820, 1670798820);'''.format(tag_id, file_or_folder_id)
        ins = db._insert(query)
        if ins[0] == -1:
            raise Exception("Error on insert to db (\"add_tag\")\n", ins[1])
        else:
            return ins[1]