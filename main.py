import sqlite3

#目前如果要重置需要把.db檔刪掉
conn = sqlite3.connect("database.db")
c = conn.cursor()
try:
    conn.execute('''
        create table records
        (
            ID      INT PRIMARY KEY  NOT NULL,
            NAME    TEXT             NOT NULL,
            VALUE   INT              NOT NULL,
            COMM    TEXT             NOT NULL
        );''')
except:
    pass
try:
    conn.execute('''
        create table targets
        (
            NAME    TEXT PRIMARY KEY NOT NULL,
            TOTAL   INT              NOT NULL
        );''')
except:
    pass

def write():#因為還沒完成所以要手動輸入，ID不要跳號不要重複
    data = [#範例
        (1, '跑步', 2000, '20190128'),
        (2, '跑步', 2000, '20190129'),
        (3, '伏地挺身', 30, '20190130')
    ]
    #如果輸入新的項目，資料庫會自動新增
    c.execute("select * from records")
    i = len(c.fetchall())
    while i < len(data):
        conn.execute("insert into records (id, name, value, comm) values({}, '{}', {}, '{}')".format(data[i][0], data[i][1], data[i][2], data[i][3]))
        c.execute("select * from targets where name = '{}'".format(data[i][1]))
        row = c.fetchone()
        if row == None:
            conn.execute("insert into targets (NAME, TOTAL) VALUES('{}', {})".format(data[i][1], data[i][2]))
        else:
            conn.execute("update targets set 'total' = {} where name = '{}'".format(row[1] + data[i][2], data[i][1]))
        conn.commit()
        i += 1
write()

def show():#顯示資料
    cursor = conn.execute("SELECT * from records")
    print("歷史記錄:")
    for row in cursor:
        for i in row:
            print(i, end='\t')
        print()
    cursor = conn.execute("SELECT * from targets")
    print("\n累計值:")
    for row in cursor:
        for i in row:
            print(i, end='\t')
        print()
show()
conn.close()