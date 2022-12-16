# import urllib2  # urllib2 is used to fetch url(s) via urlopen()
from logging import exception

from tracemalloc import start
from attr import attrs
from bs4 import BeautifulSoup
from numpy.core.numeric import NaN   # when importing ‘Beautiful Soup’ don’t add 4.   
import requests
import datetime
import time
import random
import re
import pandas as pd
import management_file_and_folder
import management_tag

ffu = management_file_and_folder.File_and_Folder_Utility()
# si = ffu.calc_session_id()
# ffu.create_folder_on_kodbox('ahmad', 'Desktop', si)
# ffu.create_folder_on_kodbox('hasan', 'ahmad', si)
# ffu.create_file_on_kodbox('hasan.has', 'ahmad', si)
# ffu.create_file_on_kodbox('ahmad.ahm', 'ahmad', si)
# create and 
tu = management_tag.Tag_Utility()
print(tu.get_tag_list())
print(tu.create_tag('Ahmad-Tag'))
# print(tu.create_tag('nsdfo iwer'))
# tag_id = tu.create_tag("Ahmad-Tag", 'label-grey-deep')
# tu.add_tag_to_file_or_folder(31, tag_id)

"""
data = pd.read_csv('./ParsedBN.csv')

def size_cats(size_in_byte):
    KB = 1024
    MB = KB * 1024
    try:
        if size_in_byte <= 100 * KB:
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


def groups(book_name):
    regex = r"\([\w\d\s ,]+\)"
    matches = re.finditer(regex, book_name, re.MULTILINE)
    found_tags = []
    for matchNum, match in enumerate(matches, start=1):
        g = match.group().replace('(', '').replace(')', '')
        # print ("Match {} was found at {}-{}: {}".format(matchNum, match.start(), match.end(),  g))
        found_tags.append(g)
        # for groupNum in range(0, len(match.groups())):
        #     groupNum = groupNum + 1
        #     print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
    return found_tags

def split_authors(authors):
    splited_autors = []    
    for i in range(len(authors)):
        author_type = 'writer'
        try:
            regex = r"\([eE][dD][sS]*\.\)"
            matches = re.finditer(regex, authors[i], re.MULTILINE)
            match = [*matches]
            if len(match) > 0:
                authors[i] = authors[i].replace(match[0].group(), '')
                authors[i] = authors[i].split()[0]
                author_type = 'editor'
        except:
            pass
        try:
            auth = []
            a = authors[i].split(',')
            for j in range(len(a)):
                auth.append(a[j])
            
            splited_autors.append([author_type, auth])
        except:
            splited_autors.append('[Unknown]')
        
    return splited_autors

# print(data.head)
authors =         data.iloc[:,3]
book_name =       data.iloc[:,4]
ISBN =            data.iloc[:,5]
file_type =       data.iloc[:,6]
published_year =  data.iloc[:,7]
file_size =       data.iloc[:,8]
tags = []
file_size_cats = []

authors_name = authors.copy()
authors_name = split_authors(authors_name)
for i in range(1000):
    # try:
        # regex = r"\([edEDsS]+\.\)"
        # regex = r"\([\w\d\s ,\.]+\)"
        # matches = re.finditer(regex, authors[i], re.MULTILINE)
        # for matchNum, match in enumerate(matches, start=1):
            # print(match)
            # if len(match) <= 0:
            #     break
            print('\n', ' ' * 20, authors[i])
            print(authors_name[i])
            pass
    # except:
    #     pass


for i in range(len(data)):
    print("(******* {} *******)".format(i))
    book_name[i] = book_name[i].replace("({})".format(ISBN[i]), "")
    file_size_cats.append(size_cats(file_size[i]))    
    found_tags = groups(book_name[i])
    tg = []
    for ft in found_tags:
        book_name[i] = book_name[i].replace('({})'.format(ft), '')
        s = ft.split(',')
        if len(s) > 0:
            for j in range(len(s)):
                tg.append(s[j])
        else:
            tg.append(s)

    print(i, ' == ', book_name[i], '  => ', tg)
    tags.append(tg)
    if i > 10:
        break
    pass

"""

"""
page = ''
# linklist = []
pagecount = 678
startTime = time.time()
nowTime = time.time()


def insertToDB(linklist, pageIndex): 
    index = 0
    mycursor = mydb.cursor()
    errorList = []
    for lnk in linklist:
        
        index += 1
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = lnk.contents[0]
        l = 'https://link.springer.com' + lnk['href']

        sql = "INSERT INTO books (title, link, inserted_time, page_number, item_number) VALUES ('{}', '{}', '{}', {}, {})".format(title, l, currentTime, pageIndex, index)
        # val = (title, l)
        # mycursor.execute(sql, val)
        mycursor.execute(sql)

        try:

            mydb.commit()
            # print('{}saved item {} at page {}'.format(' ' * 10, index, pageIndex))
        except Exception as e:
            errorList.append({pageIndex:index})
            print('\n{}errorr on save{}\'th item at page {}\n'.format('!' * 10, index, pageIndex))
            print(e)
            continue


    if len(errorList) <= 0:
        print('{}all intems saved in page {}'.format(' ' * 10, pageIndex))
    else:
        print('{}error on page {} at these items {}'.format(' ' * 10, pageIndex, errorList))

mycursor = mydb.cursor()
mycursor.execute("select `page_number` from `books` order by `id` desc limit 1")
myresult = mycursor.fetchone()
# print(myresult[0]+1)

# start = 1
start = myresult[0]+1
for i in range(start, pagecount):
    print('**** start fetch {}\'th page of {}'.format(i, pagecount - 1))
    # r = random.randint(2, 7)
    # time.sleep(r)
    try:
        page = requests.get(url.format(i))

        if page.status_code != 200:
            continue

        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a', href=True, attrs={'class': 'title'})
        linklist = []
        for l in links:
            linklist.append(l)
        print('''{}'th page fetched in {} ms and {} pages fetch in {} seconds, avg = {:.2f}'''
            .format(i, int((time.time() - nowTime) * 1000), i, int(time.time() - startTime), (time.time() - startTime)/i, 2))
        insertToDB(linklist, i)
    except Exception as e:
        print('exception in {}\'th page: ', e)
        continue
    finally:
        nowTime = time.time()

fetchTime = time.time()

print('All of pages fetched in {} seconds'.format(fetchTime - startTime))
   

insertTime = time.time()
print('''Fetch time is {} seconds\ninsert to db in {} seconds\nfetch and insert to db is {} seconds.'''
    .format(int(fetchTime), int(insertTime - fetchTime), int(insertTime - startTime)))
"""