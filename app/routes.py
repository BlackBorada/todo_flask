from flask import render_template
from app import app


@app.route("/")
def index():
    return render_template("index.html")


# @app.route('/set_database/<database>', methods=['POST', 'GET'])
# def set_database(database):
#     tasks = Task.query.all()
#     if database == 'postgresql':
#         app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_DATABASE_URI
#     elif database == 'sqlite':
#         app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_DATABASE_URI
#     else:
#         raise ValueError('Invalitd database')


#     db.drop_all()
#     db.create_all()

#     for task in tasks:
#         new_task = Task(
#             title=task.title,
#             description=task.description,
#             due_date=task.due_date,
#             completed=task.completed
#         )
#         db.session.add(new_task)
#     db.session.commit()

#     return redirect(url_for('index'))
