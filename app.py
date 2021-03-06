from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


def get_cursor():
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': '880417',
        'db': 'tutorials',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**config)
    conn.autocommit(1)  # conn.autocommit(True)
    return conn.cursor()


@app.route('/')
def index():
    return render_template("1.html")

@app.route('/1')
def index2():
    return render_template("1.html")

@app.route('/login', methods=['post'])
def login():
    name = request.form.get("name")
    password = request.form.get("password")
    print(name)
    print(password)
    cursor = get_cursor()  # 打开数据库
    row = cursor.execute("select * from tutorials.manage where name = %s", (name))  # 获取查询到的信息条数
    if row:
        cursor.execute("select password from tutorials.manage where name = %s", (name))
        message = cursor.fetchone()
        print(message[0])
        print(password)
        if password == str(message[0]):
            cursor.execute("select * from tutorials.list")
            lists = cursor.fetchall()
            return render_template("manage.html", name=name, lists=lists)
        else:
            msg = "密码错误！"
            return render_template("index.html", msg=msg)
    else:
        msg = "您不是管理员！"
        return render_template("index.html", msg=msg)


@app.route('/insert', methods=['post'])
def insert():
    id = request.form.get("id")
    name = request.form.get("name")
    age = request.form.get("age")
    home = request.form.get("home")
    identity = request.form.get("identity")
    course = request.form.get("course")

    cursor = get_cursor()  # 打开数据库
    value = (id, name, age, home, identity, course)
    insert_sql = '''INSERT INTO tutorials.list(id, name, age, home, identity, course) values (%s,%s,%s,%s,%s,%s)'''

    cursor.execute(insert_sql, value)  # 执行sql语句
    msg="添加成功！"
    return msg


@app.route('/delete/<int:id>')
def delete(id):
    cursor = get_cursor()  # 打开数据库
    cursor.execute("delete from tutorials.list where id = %s", (id))  # 删除某一行值
    msg="删除成功！"
    return msg


@app.route('/update',methods=['post'])
def update():
    id = request.form.get("id")
    name = request.form.get("name")
    age = request.form.get("age")
    home = request.form.get("home")
    identity = request.form.get("identity")

    cursor = get_cursor()  # 打开数据库
    value = (id, name, age, home, identity)

    cursor.execute("update tutorials.list set name = %s,age = %s,home =%s,identity = %s", value)
    msg = "编辑成功！"
    return msg

if __name__ == '__main__':
    app.run()
