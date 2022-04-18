from flask import Flask, render_template, request, redirect #To create Flask app, we need to import Flask package
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#Flask uses the location of the modulepassed here as a starting poinrt when it needs to load associated resources such as template files
#Instance of class Flask
app = Flask(__name__) #reference to this file, set up an application. __name__ predefined variable, which is set to the name of the module in which it is used
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) #initializing the database

#Data model
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) #what holds each task, 200 characters, no empty cells
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#index route (to avoid 404)
#routes are the different URLs that the appication implements

@app.route('/', methods=['POST', 'GET']) #URL string of the route
def index(): #function for the route
    if request.method == "POST":
        task_content = request.form['content'] #Not JSON encoded
        new_task = ToDo(content=task_content) #new task from the input
        try:
            db.session.add(new_task)
            db.session.commit()
            #redirect back to the index page
            return redirect('/')
        except:
            return "Error happened creating a task"
    else:
        return render_template('index.html')

@app.route('/todo') #URL string of the route
def index2(): #function for the route
    tasks = ToDo.query.order_by(ToDo.date_created).all()
    return render_template('todo.html', tasks=tasks) #renders from the template

@app.route('/todo/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was an error deleting the task'

@app.route('/todo/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
    
#Flask uses port 5000, but you can change it - by passing it as an argument
if __name__ == "__main__": #
    app.run(debug=True) #if any errors