import management_file_and_folder as mff
import pandas as pd
import re
import math

data = pd.read_csv('./ParsedBN.csv')

# folders = 0, authors = 3, book_name = 4, ISBN = 5, file_type = 6, published_year = 7, file_size = 8 
data_list = data.values.tolist() 
tags = []
file_size_cats = []

def parse_and_split_folders(data_list):
    for dl in data_list:
        folder = dl[0]
        temp = folder.split('/')
        # temp.insert(0, "Folders")
        # temp.insert(0, folder)
        dl[0] = temp

def parse_and_split_authors(data_list):
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

def groups(book_name):
    # ., +, *, ?, ^, $, (, ), [, ], {, }, |, \.
    regex = r"\([\w\d\s ,\.#&'-]+\)"
    matches = re.finditer(regex, book_name, re.MULTILINE)
    found_tags = []
    for matchNum, match in enumerate(matches, start=1):
        g = match.group().replace('(', '').replace(')', '')
        found_tags.append(g)
    return found_tags

def parse_file_name_and_fetch_details(data_list):
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
        # book_name = book_name.replace("({})".format(ISBN), "")
        found_tags = groups(book_name.replace("({})".format(ISBN), ""))
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

def size_cat(size_in_byte):
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

def size_categorizing(data_list):
    # dl[8] = file_size
    for dl in data_list:
        file_size = dl[8]
        size_category = size_cat(file_size)
        dl.append(size_category)

parse_and_split_folders(data_list)
parse_and_split_authors(data_list)
parse_file_name_and_fetch_details(data_list)
size_categorizing(data_list)

# index = 0
# for i in data_list:
#     index += 1
#     if index < 110:
#         continue
#     if index > 120 :
#         break
#     print(i[4], '\n\n')

def insert_to_db(data_list):
    ffu = mff.File_and_Folder_Utility()
    ru = mff.Relation_Utility()
    si = ffu.calc_session_id()
    documents_folder_id = ffu.create_folder_on_kodbox('Documents', 'Desktop', si)
    books_folder_id        = ffu.create_folder_on_kodbox_with_parent_id('Books', documents_folder_id[0], si)
    details_folder_id      = ffu.create_folder_on_kodbox_with_parent_id('Details', documents_folder_id[0], si)
    size_cats_folder_id    = ffu.create_folder_on_kodbox_with_parent_id('Size categories', details_folder_id[0], si)
    years_folder_id        = ffu.create_folder_on_kodbox_with_parent_id('Years', details_folder_id[0], si)
    types_folder_id        = ffu.create_folder_on_kodbox_with_parent_id('Types', details_folder_id[0], si)
    authors_folder_id      = ffu.create_folder_on_kodbox_with_parent_id('Authors', details_folder_id[0], si)
    #_id 
    writers_folder_id = ffu.create_folder_on_kodbox_with_parent_id('Writers', authors_folder_id[0],si)
    editors_folder_id = ffu.create_folder_on_kodbox_with_parent_id('Editors', authors_folder_id[0],si)
    #_id 
    properties_folder_id = ffu.create_folder_on_kodbox_with_parent_id('Properties', details_folder_id[0], si)    


    # folders_folder_id      = ffu.create_folder_on_kodbox_with_parent_id('Folders', documents_folder_id[0], si)
    index = 0
    data_list_count = len(data_list)
    for dl in data_list:
        index += 1
        # change index for ignore items and start add folder from this index
        if index < 0:
           continue
        # if index > 120 :
        #     break
        print('Item    {}    from   {}'.format(index, data_list_count))
        folders = dl[0]
        # is_folder     = dl[1]
        properties       = dl[2]
        authors       = dl[3]
        book_name     = dl[4]
        ISBN          = dl[5]
        file_type     = dl[6]
        year          = dl[7]
        # size_byte     = dl[8]
        # size_megabyte = dl[9]
        size_cat      = dl[10]
        
        parent_id = books_folder_id
        for f in folders:
            parent_id = ffu.create_folder_on_kodbox_with_parent_id(f, parent_id[0], si)
            # print(f)
        # 1st property book name
        book_id = ffu.create_file_on_kodbox_with_parent_id(book_name, parent_id[0], si)
        # print('book_id', book_id)
        
        # 2nd property properties of book
        properties_id_list = []
        for prop in properties:
            properties_id_list.append(ffu.create_folder_on_kodbox_with_parent_id(prop, properties_folder_id[0], si))
        
        # 3th property authors list
        authors_id_list = []
        if authors == 'Unknown':
            authors_id_list.append(ffu.create_folder_on_kodbox_with_parent_id(authors, authors_folder_id[0], si))
        else:
            for auth in range(len(authors[1])):
                if authors[0] == 'editors':
                    authors_id_list.append(ffu.create_folder_on_kodbox_with_parent_id(auth, editors_folder_id[0], si))
                elif authors[0] == 'writers':
                    authors_id_list.append(ffu.create_folder_on_kodbox_with_parent_id(auth, writers_folder_id[0], si))
        # 4th property file type
        file_type_id = ffu.create_folder_on_kodbox_with_parent_id(file_type, types_folder_id[0], si)

        # 5th property year
        year_id = ffu.create_folder_on_kodbox_with_parent_id(year, years_folder_id[0], si)

        # 6th property size category
        size_cat_id = ffu.create_folder_on_kodbox_with_parent_id(size_cat, size_cats_folder_id[0], si)

        # add relation book and properties
        # print(properties_id_list)
        for pil in properties_id_list:
            # print(dil[0])
            # print(book_id)
            ru.add_relation(book_id[0], pil[0])
            ru.add_relation(pil[0], book_id[0])
        # print(300)
        # add relation book and authors(editors/writers)
        for ail in authors_id_list:
            ru.add_relation(book_id[0], ail[0])
            ru.add_relation(ail[0], book_id[0])
        # add relation book and file type
        ru.add_relation(book_id[0], file_type_id[0])
        ru.add_relation(file_type_id[0], book_id[0])
        # add relation book and year
        ru.add_relation(book_id[0], year_id[0])
        ru.add_relation(year_id[0], book_id[0])
        # add relation book and size category
        ru.add_relation(book_id[0], size_cat_id[0])
        ru.add_relation(size_cat_id[0], book_id[0])

insert_to_db(data_list)

# df = pd.DataFrame (data_list, columns = ['folder', 'is_folder', 'details', 'authors', 'book_name', 'ISBN',
#                                         'type', 'year', 'size_byte', 'sixe_megabyte', 'size_cat' ])
# df.to_csv("./file.csv", sep=',',index=False)
