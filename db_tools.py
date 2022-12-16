import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database = 'kodbox'
    )

def _insert(query, db = mydb, be_commit = True):
    mycursor = db.cursor()
    mycursor.execute(query)
    try:
        if be_commit == True:
            db.commit()
        msg = '+Insert {} row(s) to table.'.format(mycursor.rowcount)
        return (msg, mycursor.lastrowid, mycursor.rowcount)
    except Exception as e:
        print('\n{}errorr on insert to db with below query:{}\n{}error:\n{}'.format('!' * 10, query, '*' * 10, e))
        return (-1, e)

def _update(query, db = mydb, be_commit = True):
    mycursor = db.cursor()
    mycursor.execute(query)
    try:
        if be_commit == True:
            db.commit()
        msg = '*Update {} row(s) to table.'.format(mycursor.rowcount)
        return (msg, mycursor.rowcount)
    except Exception as e:
        print('\n{}errorr on update to db with below query:{}\n{}error:\n{}'.format('!' * 10, query, '*' * 10, e))
        return (-1, e)

def _select(query, db = mydb):
    mycursor = db.cursor()
    mycursor.execute(query)
    records = mycursor.fetchall()
    try:
        msg = '#Select {} row(s) from table.'.format(mycursor.rowcount)
        return (msg, mycursor.rowcount, records)
    except Exception as e:
        print('\n{}errorr on select to db with below query:{}\n{}error:\n{}'.format('!' * 10, query, '*' * 10, e))
        return (-1, e)

def _delete(query, db = mydb, be_commit = True):
    mycursor = db.cursor()
    mycursor.execute(query)
    try:
        if be_commit == True:
            db.commit()
        msg = '-Deleted {} row(s) from table.'.format(mycursor.rowcount)
        return (msg, mycursor.rowcount)
    except Exception as e:
        print('\n{}errorr on delete to db with below query:{}\n{}error:\n{}'.format('!' * 10, query, '*' * 10, e))
        return (-1, e)