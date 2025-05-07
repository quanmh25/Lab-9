from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask('meow_task', template_folder='Practice/instance')
           
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'prac.db') # Sử dụng SQL làm cơ sở dữ liệu và lưu file

db = SQLAlchemy(app) # SQLAlchemy giúp bạn tương tác vs csdl trong python mà k cần truy vấn trực tiếp
migrate = Migrate(app, db) # Giúp theo dõi và áp dụng các thay đổi cho csdl (thêm bảng, cột,...)


# tasks = [
#     {'todo': 'row 1',
#      'deadline' : '04.04.2025',
#      'ready' : False,
#      'id' : 0},
#      {'todo': 'row 2',
#      'deadline' : '04.04.2025',
#      'ready' : False,
#      'id' : 1},
#      {'todo': 'row 3',
#      'deadline' : '04.04.2025',
#      'ready' : False,
#      'id' : 2}
# ]

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(500))
    deadline = db.Column(db.String(20))
    ready = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task{self.id} / {self.deadline}> {self.todo}'
    


@app.route('/')
def main():
    tasks = Task.query.all()                # Truy vấn các dòng từ bảng Task trong csdl 
    print(tasks)
    return render_template('index.html', task_list=tasks)        # Trả về file html làm giao diện


# Endpoint để cchỉnh sửa trạng thái hoàn thành của 1 nhiệm vụ dựa trên task_idid
@app.route('/ready/<int:task_id>', methods=['PATCH'])       # Đoạn task_id  trong URL là 1 số nguyên đại diện cho task cần sửa đổi
def modify_task(task_id):
    task = Task.query.get(task_id)                  # Tìm nhiệm vụ trong bảng với id đã đưa
    if task is None:
        return 'Task not found', 404
    task.ready = request.json['ready']            # Cập nhật trangj thái ready của nhiệm vụ 
    db.session.commit()                             # Lưu thay đổi vào csdl SQLite 
    # global tasks
    # ready = request.json['ready']
    # for task in tasks:
    #     if task['id'] == task_id:
    #         task.update({'ready': ready})
    return 'Ok'                             # Trả về phản hồi để xác nhận chỉnh sửa thành công


# Endpoint để thêm nhiệm vụ mới vào csdlcsdl
@app.route('/task', methods=['POST'])
def create_task():
    data = request.json                 # Lấy dữ liệu json từ body của yêu cầu http POST
    task = Task(**data)                 # Dữ liệu json được truyền trực tiếp để tạo đổi tượng Task
    db.session.add(task)                # Thêm nhiệm vụ mới vào 
    db.session.commit()                 # Lưu nhiệm vụ
    # last_id = task[-1]['id']
    # new_id = last_id + 1
    # data['id'] = new_id
    # tasks.append(data)
    return 'Ok'




if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)