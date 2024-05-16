import flask
import re
import pymysql
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask_cors import CORS

# 初始化
app = flask.Flask(__name__)
CORS(app)
# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='123456', database='learningmanagementsystem', charset='utf8')
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()
# 存储登陆用户的名字用户其它网页的显示
users = []

app.secret_key = 'carson1'  # 会话密钥，用于保护session


def is_logged_in():
    return 'login' in session and session['login']


def get_user_role():
    return session.get('role', None)


def get_db_cursor():
    db = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                         database='learningmanagementsystem', charset='utf8')
    return db, db.cursor()


def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='123456', db='learningmanagementsystem',
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


# def get_db_connection():
#     connection = pymysql.connect(host='localhost', user='root', password='123456', db='learningmanagementsystem')
#     cursor = connection.cursor()
#     return connection, cursor


@app.route('/')
def main():
    if not is_logged_in():
        return render_template('firstpage.html',
                               courses=get_student_courses, uploads=get_instructor_uploads)
    else:
        # 用户已登录，根据角色显示相应内容
        role = get_user_role()
        if role == 'student':
            # 学生角色，显示课程列表
            return render_template('student_homepage.html')
        elif role == 'instructor':
            # 教师角色，显示上传列表
            return render_template('instructor_homepage.html')
        elif role == 'admin':
            # 管理员角色，可以管理用户、课程和讲座
            return render_template('admin_homepage.html')
        else:
            # 未知角色或者未指定角色，重定向到登录
            return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    session['login'] = ''
    msg = ''
    user = ''
    if request.method == 'POST':
        user = request.form.get("user", "")
        pwd = request.form.get("pwd", "")
        role = request.form.get("role", "")

        if re.match(r"^[a-zA-Z]+$", user) and re.match(r"^[a-zA-Z\d]+$", pwd):
            # 定义 SQL 查询模板
            sql = "SELECT * FROM {} WHERE Name=%s AND Password=%s;"
            if role == 'admin':
                table = 'administrator'
            elif role == 'instructor':
                table = 'instructor'
            elif role == 'student':
                table = 'student'
            else:
                # msg = 'Invalid role selected'
                return render_template('login.html', msg=msg, user=user)

            # 执行参数化查询
            cursor.execute(sql.format(table), (user, pwd))
            result = cursor.fetchone()
            if result:
                session['login'] = 'OK'
                session['username'] = user  # 存储登录成功的用户名用于显示
                session['role'] = role  # 存储用户角色
                return redirect(url_for('admin_dashboard'))
            else:
                msg = 'User name or password is wrong'
        else:
            msg = 'Invalid input'

    return render_template('login.html', msg=msg, user=user)


def is_admin():
    return session.get('login') == 'OK' and session.get('role') == 'admin'


def is_instructor():
    return session.get('login') == 'OK' and session.get('role') == 'instructor'


def is_student():
    return session.get('login') == 'OK' and session.get('role') == 'student'


# 假设这是您的数据库查询函数，返回学生和教师的课程列表和上传列表
# 获取学生课程列表
@app.route('/api/courses')
def get_student_courses():
    db, cursor = get_db_cursor()
    try:
        cursor.execute("SELECT CourseID, CourseTitle, Content, CreditHours, InstructorID FROM course")
        courses = [{'CourseID': row[0], 'CourseTitle': row[1], 'Content': row[2], 'CreditHours': row[3],
                    'InstructorID': row[4]} for row in cursor.fetchall()]
        return jsonify(courses)
    except Exception as e:
        print("Failed to fetch courses:", e)
        return jsonify([]), 500
    finally:
        cursor.close()
        db.close()


@app.route('/api/uploads')
def get_instructor_uploads():
    cursor.execute("SELECT LectureID, CourseID, LectureTitle, UploadDate, Instructor FROM lecture")
    uploads = [
        {'LectureID': row[0], 'CourseID': row[1], 'LectureTitle': row[2], 'UploadDate': row[3], 'Instructor': row[4]}
        for row in cursor.fetchall()]
    return jsonify(uploads)


# 管理员页面路由
@app.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    if is_logged_in() and get_user_role() == 'admin':
        return render_template('admin_homepage.html')
    else:
        return redirect(url_for('login'))


@app.route('/admin/courses', methods=['POST', 'GET', 'PUT', 'DELETE'])
def admin_courses():
    if not session.get('role') == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    db, cursor = get_db_connection(), None
    try:
        cursor = db.cursor()
        if request.method == 'GET':
            cursor.execute("SELECT * FROM course")
            courses = cursor.fetchall()
            return jsonify(courses)

        # 确保接收的是JSON格式数据
        if not request.is_json:
            return jsonify({'error': 'Missing JSON in request'}), 400

        data = request.get_json()
        if request.method == 'POST':
            sql = "INSERT INTO course (CourseTitle, Content, CreditHours, InstructorID) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data['CourseTitle'], data['Content'], data['CreditHours'], data['InstructorID']))

        elif request.method == 'PUT':
            sql = "UPDATE course SET CourseTitle=%s, Content=%s, CreditHours=%s, InstructorID=%s WHERE CourseID=%s"
            cursor.execute(sql, (
                data['CourseTitle'], data['Content'], data['CreditHours'], data['InstructorID'], data['CourseID']))

        elif request.method == 'DELETE':
            sql = "DELETE FROM course WHERE CourseID=%s"
            cursor.execute(sql, (data['CourseID'],))

        db.commit()
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        db.close()

@app.route('/assign_instructor', methods=['POST'])
def assign_instructor():
    data = request.get_json()
    course_id = data['course_id']
    instructor_id = data['instructor_id']

    course = Course.query.filter_by(CourseID=course_id).first()
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    instructor = Instructor.query.filter_by(InstructorID=instructor_id).first()
    if not instructor:
        return jsonify({'error': 'Instructor not found'}), 404

    # 分配讲师到课程
    course.instructor = instructor
    db.session.commit()

    return jsonify({'message': 'Instructor assigned successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/admin/lectures', methods=['POST', 'GET', 'PUT', 'DELETE'])
def admin_lectures():
    if not session.get('role') == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    db, cursor = get_db_connection(), None
    try:
        cursor = db.cursor()
        if request.method == 'GET':
            cursor.execute("SELECT * FROM lecture")
            lectures = cursor.fetchall()
            return jsonify(lectures)

        data = request.json
        if request.method == 'POST':
            sql = "INSERT INTO lecture (CourseID, LectureTitle, UploadDate, Instructor) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data['CourseID'], data['LectureTitle'], data['UploadDate'], data['Instructor']))

        elif request.method == 'PUT':
            sql = "UPDATE lecture SET CourseID=%s, LectureTitle=%s, UploadDate=%s, Instructor=%s WHERE LectureID=%s"
            cursor.execute(sql, (
                data['CourseID'], data['LectureTitle'], data['UploadDate'], data['Instructor'], data['LectureID']))

        elif request.method == 'DELETE':
            sql = "DELETE FROM lecture WHERE LectureID=%s"
            cursor.execute(sql, (data['LectureID'],))

        db.commit()
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        db.close()


@app.route('/admin/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    if not session.get('role') == 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    db = get_db_connection()
    cursor = db.cursor()  # 创建游标

    try:
        print(f"Attempting to delete course with ID: {course_id}")
        cursor.execute("DELETE FROM course WHERE CourseID = %s", (course_id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'No course found'}), 404
        db.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        db.rollback()
        app.logger.error(f"Failed to delete course {course_id}: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        db.close()

#
# @app.route('/admin/courses/<int:course_id>', methods=['PUT'])
# def update_course(course_id):
#     try:
#         data = request.get_json()
#         print("Received data:", data)  # Debug print
#         db, cursor = get_db_connection()
#         cursor.execute(
#             "UPDATE course SET CourseTitle=%s, Content=%s, CreditHours=%s, InstructorID=%s WHERE CourseID=%s",
#             (data['CourseTitle'], data['Content'], data['CreditHours'], data['InstructorID'], course_id)
#         )
#         if cursor.rowcount == 0:
#             app.logger.info(f"No course found with ID {course_id}")
#             return jsonify({"error": "No course found with provided ID"}), 404
#         db.commit()
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         db.rollback()
#         app.logger.error(f"Failed to update course: {e}")
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cursor.close()
#         db.close()
@app.route('/admin/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    db = None
    cursor = None
    try:
        db = get_db_connection()  # Get the database connection
        cursor = db.cursor()      # Create cursor from database connection

        data = request.get_json()
        # Log received data for debugging purposes
        app.logger.info(f"Received data for update: {data}")

        # Perform the database update
        cursor.execute(
            "UPDATE course SET CourseTitle=%s, Content=%s, CreditHours=%s, InstructorID=%s WHERE CourseID=%s",
            (data['CourseTitle'], data['Content'], data['CreditHours'], data['InstructorID'], course_id)
        )

        # Check if the row exists and has been updated
        if cursor.rowcount == 0:
            app.logger.info(f"No course found with ID {course_id}")
            return jsonify({"error": "No course found with provided ID"}), 404

        # Commit changes if everything is fine
        db.commit()
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        # Rollback in case of any error
        if db:
            db.rollback()
        app.logger.error(f"Failed to update course {course_id}: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        # Close cursor and database connection properly
        if cursor:
            cursor.close()
        if db:
            db.close()



# 启动服务器
app.debug = True
# 增加session会话保护(任意字符串,用来对session进行加密)
app.secret_key = 'carson1'
try:
    app.run()
except Exception as err:
    print(err)
    db.close()  # 关闭数据库连接
