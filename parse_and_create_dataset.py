import management_file_and_folder as mff
import pandas as pd
import log_management as lm
import dataset_parse

data = pd.read_csv('./ParsedBN.csv')

# folders = 0, authors = 3, book_name = 4, ISBN = 5, file_type = 6, published_year = 7, file_size = 8 
data_list = data.values.tolist() 

dp = dataset_parse.DatasetParse()

# change data format for every columns and normalization them.
dp.parse_and_split_folders(data_list)
dp.parse_and_split_authors(data_list)
dp.parse_file_name_and_fetch_details(data_list)
dp.size_categorizing(data_list)

# create log file class to save logs.
log = lm.LogFile()
current_index = log.current_index()

# function for create or select requirement folders.
def create_or_select_requirement_folders(sesstion_id):
    ffu = mff.File_and_Folder_Utility()    
    
    log.write_log("Create/Select folder", "Create/Select \"Documents\" folder on Desktop and get this id.")
    documents_folder_id = ffu.create_folder_on_kodbox('Documents', 'Desktop', sesstion_id)
    
    log.write_log("Create/Select folder", "Create/Select \"Books\" folder in Desktop\\Document folder and get this id.")
    books_folder_id        = ffu.create_folder_on_kodbox_with_parent_id('Books', documents_folder_id[0], sesstion_id)
    
    log.write_log("Create/Select folder", "Create/Select \"Details\" folder in Desktop\\Document folder and get this id.")
    details_folder_id      = ffu.create_folder_on_kodbox_with_parent_id('Details', documents_folder_id[0], sesstion_id)
    
    log.write_log("Create/Select folder", "Create/Select \"Size categories\" folder in Desktop\\Documents\\Details folder and get this id.")
    size_cats_folder_id    = ffu.create_folder_on_kodbox_with_parent_id('Size categories', details_folder_id[0], sesstion_id)
    
    log.write_log("Create/Select folder", "Create/Select \"Years\" folder in Desktop\\Documents\\Details folder and get this id.")
    years_folder_id        = ffu.create_folder_on_kodbox_with_parent_id('Years', details_folder_id[0], sesstion_id)
    
    log.write_log("Create/Select folder", "Create/Select \"Types\" folder in Desktop\\Documents\\Details folder and get this id.")
    types_folder_id        = ffu.create_folder_on_kodbox_with_parent_id('Types', details_folder_id[0], sesstion_id)
    
    log.write_log("Create/Select folder", "Create/Select \"Authors\" folder in Desktop\\Documents\\Details folder and get this id.")
    authors_folder_id      = ffu.create_folder_on_kodbox_with_parent_id('Authors', details_folder_id[0], sesstion_id)
    #_id 
    
    log.write_log("Create/Select folder", "Create/Select \"Writers\" folder in Desktop\\Documents\\Details\\Authors folder and get this id.")
    writers_folder_id = ffu.create_folder_on_kodbox_with_parent_id('Writers', authors_folder_id[0],sesstion_id)
    
    log.write_log("Create/Select folder", "Create/Select \"Editors\" folder in Desktop\\Documents\\Details\\Authors folder and get this id.")
    editors_folder_id = ffu.create_folder_on_kodbox_with_parent_id('Editors', authors_folder_id[0],sesstion_id)
    #_id 
    
    log.write_log("Create/Select folder", "Create/Select \"Properties\" folder in Desktop\\Documents\\Details folder and get this id.")
    properties_folder_id = ffu.create_folder_on_kodbox_with_parent_id('Properties', details_folder_id[0], sesstion_id) 
    return books_folder_id, size_cats_folder_id, years_folder_id, types_folder_id, authors_folder_id, writers_folder_id, editors_folder_id, properties_folder_id

# function for create relation between entities like, books, folders, authors and etc.
def create_relations(book_id, properties_id_list, authors_id_list, file_type_id, year_id, size_cat_id):
    ru = mff.Relation_Utility()
    # add relation book and properties
    for pil in properties_id_list:
        log.write_log("Create relation", "Create relation between id\'s {} and {}".format(book_id[0], pil[0]))
        ru.add_bi_directional_relation(book_id[0], pil[0])
    # add relation book and authors(editors/writers)
    for ail in authors_id_list:
        log.write_log("Create relation", "Create relation between id\'s {} and {}".format(book_id[0], ail[0]))
        ru.add_bi_directional_relation(book_id[0], ail[0])
    # add relation book and file type
    log.write_log("Create relation", "Create relation between id\'s {} and {}".format(book_id[0], file_type_id[0]))
    ru.add_bi_directional_relation(book_id[0], file_type_id[0])
    # add relation book and year
    log.write_log("Create relation", "Create relation between id\'s {} and {}".format(book_id[0], year_id[0]))
    ru.add_bi_directional_relation(book_id[0], year_id[0])
    # add relation book and size category
    log.write_log("Create relation", "Create relation between id\'s {} and {}".format(book_id[0], size_cat_id[0]))
    ru.add_bi_directional_relation(book_id[0], size_cat_id[0])

# function for save dataset file list to database
def insert_to_db(data_list):
    ffu = mff.File_and_Folder_Utility()
    si = ffu.calc_session_id()   
    print(10)
    books_folder_id, size_cats_folder_id, years_folder_id, types_folder_id, \
        authors_folder_id, writers_folder_id, editors_folder_id, \
        properties_folder_id = create_or_select_requirement_folders(si)

    index = 0
    data_list_count = len(data_list)
    print(11)
    for dl in data_list:
        index += 1
        log.write_index(index)
        # change index for ignore items and start add folder from this index
        if index < current_index:
           continue
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
        log.write_log("Create/Select folder", "Create/Select parent folder of book = {}.".format(folders))
        for f in folders:
            parent_id = ffu.create_folder_on_kodbox_with_parent_id(f, parent_id[0], si)

        # 1st property book name
        log.write_log("Create/Select file", "Create/Select book\'s file = \"{}\".".format(book_name))
        book_id = ffu.create_file_on_kodbox_with_parent_id(book_name, parent_id[0], si)
        
        # 2nd property properties of book
        properties_id_list = []
        for prop in properties:
            log.write_log("Create/Select folder", "Create/Select book\'s property = \"{}\".".format(prop))
            properties_id_list.append(ffu.create_folder_on_kodbox_with_parent_id(prop, properties_folder_id[0], si))
        
        # 3th property authors list
        authors_id_list = []
        if authors == 'Unknown':
            log.write_log("Create/Select folder", "Create/Select book\'s unknown author = \"{}\".".format(authors))
            authors_id_list.append(ffu.create_folder_on_kodbox_with_parent_id(authors, authors_folder_id[0], si))
        else:
            for auth in range(len(authors[1])):
                if authors[0] == 'editors':
                    log.write_log("Create/Select folder", "Create/Select book\'s editor = \"{}\".".format(auth))
                    authors_id_list.append(ffu.create_folder_on_kodbox_with_parent_id(auth, editors_folder_id[0], si))
                elif authors[0] == 'writers':
                    log.write_log("Create/Select folder", "Create/Select book\'s writer = \"{}\".".format(auth))
                    authors_id_list.append(ffu.create_folder_on_kodbox_with_parent_id(auth, writers_folder_id[0], si))

        # 4th property file type
        log.write_log("Create/Select folder", "Create/Select book\'s file type = \"{}\".".format(file_type))
        file_type_id = ffu.create_folder_on_kodbox_with_parent_id(file_type, types_folder_id[0], si)

        # 5th property year
        log.write_log("Create/Select folder", "Create/Select book\'s year published = \"{}\".".format(year))
        year_id = ffu.create_folder_on_kodbox_with_parent_id(year, years_folder_id[0], si)

        # 6th property size category
        log.write_log("Create/Select folder", "Create/Select book\'s size category = \"{}\".".format(size_cat))
        size_cat_id = ffu.create_folder_on_kodbox_with_parent_id(size_cat, size_cats_folder_id[0], si)
        
        # Create relation for files and folders that created.
        create_relations(book_id, properties_id_list, authors_id_list, file_type_id, year_id, size_cat_id)

insert_to_db(data_list)