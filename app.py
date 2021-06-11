from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(
    db.Model):  # the id and data_created is auto generated, so only content needs to be defined for creating an instance
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return 'Task %I' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # 'content' is the name of an input field
        new_task = Todo(content=task_content)  # to grab the content to form a new task

        try:
            db.session.add(new_task)
            db.session.commit()

            return redirect('/')
        except:
            return 'There was an issue adding new task.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasklist=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is something wrong when deleting the task.'


@app.route('/update/<int:id>', methods = ["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There are some trouble updating the task"
    else:
        return render_template('update.html', task = task)


if __name__ == '__main__':
    app.run(debug=True)
