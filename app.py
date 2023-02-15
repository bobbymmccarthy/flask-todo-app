from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#application factories
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

        
#routing 
@app.route('/')
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list = todo_list)

#routing
@app.route('/about')
def about():
    return 'About'

#routing
@app.route('/add', methods = ["POST"])
def add():
    title = request.form.get('title')
    #application context and application factories
    with app.app_context():
        new_todo = Todo(title = title)
        db.session.add(new_todo)
        db.session.commit()
    #redirection
    return redirect(url_for('index'))

#routing
@app.route('/update/<int:todo_id>')
def update(todo_id):
    title = request.form.get('title')
    #application context and application factories
    with app.app_context():
        #database query
        todo = Todo.query.filter_by(id=todo_id).first()
        todo.complete = not todo.complete
        db.session.commit()

    #redirection
    return redirect(url_for('index'))

#routing
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    title = request.form.get('title')
    #application context and application factories
    with app.app_context():
        #database query
        todo = Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()

    #redirection
    return redirect(url_for('index'))

if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    #     new_todo = Todo(title = "todo 1", complete = False)
    #     db.session.add(new_todo)
    #     db.session.commit()

    app.run(debug = True)