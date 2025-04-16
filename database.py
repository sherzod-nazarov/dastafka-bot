from sqlite3 import connect, Error


def SavatClear(user_id):
    try:
        c = connect("savat.db")
        cursor = c.cursor()
        cursor.execute("delete from savat  where user_id=?", (user_id,))
        c.commit()
    except (Error, Exception) as eror:
        print(eror)
    finally:
        if c:
            cursor.close()
            c.close()



def AddSavat(name, narxi, count, user_id):
    try:
        c = connect("savat.db")
        cursor = c.cursor()
        cursor.execute("insert into savat(name, narxi, count, user_id) values(?, ?, ?, ?)", (name, narxi, count, user_id))
        c.commit()
    except (Error, Exception) as eror:
        print(eror)
    finally:
        if c:
            cursor.close()
            c.close()


def ReadSavat(id):
    try:
        c = connect("savat.db")
        cursor = c.cursor()
        cursor.execute("select * from savat where user_id=?", (id,))
        malumot = cursor.fetchall()
        return malumot
    except (Error, Exception) as eror:
        print(eror)
    finally:
        if c:
            cursor.close()
            c.close()








# try:
#     c = connect("savat.db")
#     cursor = c.cursor()
#     cursor.execute("""
#                 create table savat(
#                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                    name text not null,
#                    narxi real not null,
#                    count integer not null,
#                    user_id integer not null
#                    );
#                 """)
#     c.commit()
# except (Error, Exception) as eror:
#     print(eror)
# finally:
#     if c:
#         cursor.close()
#         c.close()

