import re
import math

# columns index by default
# folders = 0, authors = 3, book_name = 4, ISBN = 5, file_type = 6, published_year = 7, file_size = 8 
class DatasetParse():

    def parse_and_split_folders(self, data_list, col_num=0):
        for dl in data_list:
            folder = dl[0]
            temp = folder.split('/')
            dl[0] = temp

    def parse_and_split_authors(self, data_list, col_num = 3):
        for dl in data_list:
            author = dl[3]
            splited_autors = []    
            author_type = 'writers'
            try:
                regex = r"\([eE][dD][sS]*\.\)"
                matches = re.finditer(regex, dl[3], re.MULTILINE)
                match = [*matches]
                if len(match) > 0:
                    author = author.replace(match[0].group(), '')
                    author = author.split()[0]
                    author_type = 'editors'
            except:
                pass
            try:
                auth = []
                a = author.split(',')
                for j in range(len(a)):
                    auth.append(a[j])
                
                splited_autors.append([author_type, auth])
            except:
                splited_autors.append('Unknown')
            dl[3] = splited_autors[0]

    def __groups(self, book_name):
        # ., +, *, ?, ^, $, (, ), [, ], {, }, |, \.
        regex = r"\([\w\d\s ,\.#&'-]+\)"
        matches = re.finditer(regex, book_name, re.MULTILINE)
        found_tags = []
        for matchNum, match in enumerate(matches, start=1):
            g = match.group().replace('(', '').replace(')', '')
            found_tags.append(g)
        return found_tags

    def parse_file_name_and_fetch_details(self, data_list, col_num = 2):
        # dl[2] = file_name
        # dl[4] = book_name
        for dl in data_list:
            book_name = dl[4]
            if type(book_name) != type('string'):
                continue
            ISBN = dl[5]
            file_type = dl[6]
            if type(ISBN) is not str:
                ISBN = ''
            if type(file_type) is not str:
                file_type = ''
            else:
                file_type = '.' + file_type
            # Remove ISBN from book_name
            found_tags = self.__groups(book_name.replace("({})".format(ISBN), ""))
            tg = []
            for ft in found_tags:
                # book_name = book_name.replace('({})'.format(ft), '')
                s = ft.split(',')
                if len(s) > 0:
                    for j in range(len(s)):
                        tg.append(s[j])
                else:
                    tg.append(s)
            dl[2] = tg

    def __size_cat(self, size_in_byte):
        KB = 1024
        MB = KB * 1024
        
        try:
            if math.isnan(size_in_byte):
                return 'Unknown'
            elif size_in_byte <= 100 * KB:
                return 'Less than 100 KB'
            elif (size_in_byte > 100 * KB) and (size_in_byte <= 200 * KB):
                return 'Between 100 and 200 KB'
            elif (size_in_byte > 200 * KB) and (size_in_byte <= 500 * KB):
                return 'Between 200 and 500 KB'
            elif (size_in_byte > 500 * KB) and (size_in_byte <= 1 * MB):
                return 'Between 0.5 and 1 MB'
            elif (size_in_byte > 1 * MB) and (size_in_byte <= 2 * MB):
                return 'Between 1 and 2 MB'
            elif (size_in_byte > 2 * MB) and (size_in_byte <= 5 * MB):
                return 'Between 2 and 5 MB'
            elif (size_in_byte > 5 * MB) and (size_in_byte <= 10 * MB):
                return 'Between 5 and 10 MB'
            elif (size_in_byte > 10 * MB) and (size_in_byte <= 50 * MB):
                return 'Between 10 and 50 MB'
            elif (size_in_byte > 50 * MB) and (size_in_byte <= 100 * MB):
                return 'Between 50 and 100 MB'
            elif (size_in_byte > 100 * MB) and (size_in_byte <= 500 * MB):
                return 'Between 100 and 500 MB'
            else:
                return 'Greater than 500 MB'
        except:
            return 'Unknown'

    def size_categorizing(self, data_list, col_num = 8):
        # dl[8] = file_size
        for dl in data_list:
            file_size = dl[col_num]
            size_category = self.__size_cat(file_size)
            dl.append(size_category)