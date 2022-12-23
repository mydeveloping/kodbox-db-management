# kodbox-db-management
Create and management folders, files, tags, and relations in kodbox db with python.

This project create for my teacher excercise's for Data visualization class.

My teacher Dr. M.B. Ghaznavi Ghooshchi issue this project.

# How to use.
```
1- download this project.
2- Extract file to a folder.
3- Open terminal/CMD and go to project folder.
4- Write below code:
python parse_and_create_dataset.py
```
Note: You can use your data to import to kodbox. You only follow csv file like "ParsedBN.csv".
Note2: If you don't use mysql default config, must change config from Database in "db_tools.py ".

# Files and containing functions internal:

## In db_tools.py

### function \_insert:

Use \_insert function to run your insert queries like below.
\_insert({your query string}, {[an instance of db]}, {[say this command is a transaction or no]})

Definition:
```python
def _insert(query, db = mydb, be_commit = True):
```

Params:

query: Your query string that you want run it.
db: A instant from mysql.connector.connect
be_commit: Define that your command be a single query or multi command query.

Return:

If query command hasn't any exception, return a tuple contain insert message, and last inserted row id, and row count that affected.
But if query command, raise an exception, print a string that contain exception message, and return a tuple that contain -1 and exception message.


Example:
```python
int1 = 123
str1 = 'test'
str2 = 'string value'
query = """INSERT INTO table1 (col1, col2, col3) VALUES ({val1},'{val2}','{val3}')""".format(val1 = int1, val2 = str1, val3 = str2)
ins = _insert(query, mydb)
print(ins)
```

### function \_update:

Use \_update function to run your insert queries like below.

\_update({your query string}, {[an instance of db]}, {[say this command is a transaction or no]})

Definition:
```python
def _update(query, db = mydb, be_commit = True):
```

Params:

query: Your query string that you want run it.
db: A instant from mysql.connector.connect
be_commit: Define that your command be a single query or multi command query.

Return:

If query command hasn't any exception, return a tuple contain insert message, and row count that affected.
But if query command, raise an exception, print a string that contain exception message, and return a tuple that contain -1 and exception message.


Example:
```python
int1 = 123
str1 = 'test'
str2 = 'string value'
query = """UPDATE table1 SET col1 = {}, col2 = '{}', col3 = '{}'""".format(int1, str1, str2)
update = _update(query, mydb)
print(update)
```

### function \_select:

Use \_select function to run your insert queries like below.

\_select({your query string}, {[an instance of db]})

Definition:
```python
def _select(query, db = mydb):
```

Params:

query: Your query string that you want run it.
db: A instant from mysql.connector.connect

Return:

If query command hasn't any exception, return a tuple contain insert message, and row count fetched, a tuple that contain all of records that fetched.
But if query command, raise an exception, print a string that contain exception message, and return a tuple that contain -1 and exception message.


Example:
```python
query = "SELECT * FROM table1 WHERE id > 10"
sel = _select(query, mydb)
print(sel)
```

### function \_delete:

Use \_delete function to run your insert queries like below.

\_delete({your query string}, {[an instance of db]}, {[say this command is a transaction or no]})

Definition:
```python
def _delete(query, db = mydb, be_commit = True):
```

Params:

query: Your query string that you want run it.
db: A instant from mysql.connector.connect
be_commit: Define that your command be a single query or multi command query.

Return:

If query command hasn't any exception, return a tuple contain insert message, and row count that affected.
But if query command, raise an exception, print a string that contain exception message, and return a tuple that contain -1 and exception message.


Example:
```python
query = "DELETE FROM table1 WHERE id = 123"
del = _delete(query, mydb)
print(del)
```

## In management_file_and_folder.py

This module contain two classes call "Relation_Utility" and "File_and_Folder_Utility".

"Relation_Utility" class use for create relation between file and file, file and folder, folder and folder, and viceversa.
"File_and_Folder_Utility" class use for create file and/or folder.

Many functions in this module are protected, and only functions that create file, folder or relation are public.

### Relation_Utility class

For add a relation you must create an instance of this class, and call "add_relation" method and pass source "sourceID" and destination "sourceID" of relation to this method.

For example, if "sourceID" of "Folder1" be 123 and "sourceID" of "Folder2" be 456: below command create a relation between these folders:
```python
ru = Relation_Utility()
rel_id = ru.add_relation(123, 456)
```
"rel_id" variable is Identification of this relation.

### File_and_Folder_Utility class

This class use for create a file or folder. For create a file, you can use two method, "create_file_on_kodbox" and "create_file_on_kodbox_with_parent_id".

Public method in this class are:


"calc_session_id" method:
A session ID is a 32 characters lenght of string that create with this regex formula: [A-Za-z0-9_]{32}. Use this method for create a unique session id. 

"create_file_on_kodbox" method:
Give three parameters, "file_name", "parent_id", "session_id". Both of "file_name" and "parent_name" are string, and "sesstion_id" is a number for current session identification. "file_name" is name for your file name, "parent_name" is a folder name, that you want create your file into this.

"create_file_on_kodbox_with_parent_id" method:
Give three parameters, "file_name", "parent_id", "session_id". Parameters for this method same of the "create_file_on_kodbox" method, and "parent_id" is "sourceID" of parent folder.

"create_file_on_kodbox" method:
like "create_file_on_kodbox" but for create folder.

"create_file_on_kodbox_with_parent_id" method:
like "create_file_on_kodbox_with_parent_id" but for create folder.

## In management_tag.py

This module a calss that call "Tag_Utility" for create tag, assign a tag to a file or folder, fetch tag list and found is there a tag name in tag list. 


### Tag_Utility class

For use feature of this class you must create an instance of this class.

"get_tag_list" method:
This method return a list that contain tag names exist in DB.

For example:

```python
tu = Tag_Utility()
tag_list = tu.get_tag_list()
```
tag_list variable has a list of tag name in your kodbox tags.

"is_tag_name_exist" method:
This method use for check any tag name. You only pass a name with parameter to this function, then if your name exist in DB, this function return True, else return False.

For example:

```python
tu = Tag_Utility()
t = tu.is_tag_name_exist('test')
```
If there is a tag with "test" name, then t has True value, else t is False.

"create_tag" method:
This method use for create a tag to kodbox. This method has two parameters called "tag_name" and "tag_color".
"tag_name" is your tag name, and "tag_color" is your color for this tag. If you don't select any color, "tag_name" has a default value.

For example:

```python
tu = Tag_Utility()
tag1 = tu.create_tag('with set color', 'label-red-deep')
tag2 = tu.create_tag('without set color')
```
"tag1" variable has an ID for tag name "with set color" with selected color, and "tag2" variable has an ID for tag name "without set color" with default color.
Note: If selected tag name exist in DB, this method return Id of existed tag name.

"add_tag_to_file_or_folder" method:
This is method use for assign a tag to folder or file. First parameter of this method is "file_or_folder_id" for id of source value, and second parameter is "tag_id" that point to selected tag.

For example:
```python
tu = Tag_Utility()
id = tu.add_tag_to_file_or_folder(12, 10)
```
This command assign tag with id = 10 to a file or folder (source) with 12, and "id" variable has an id from this relation.
