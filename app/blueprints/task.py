from flask import flash, render_template, redirect, url_for
from flask import Blueprint
from flask_login import current_user, login_required
from flask.views import MethodView

from app import db
from app.models import Task, Users
from app.forms import TaskForm


task_bp = Blueprint("task", __name__)


class TaskList(MethodView):
    def get(self):
        form = TaskForm()
        tasks = (
            Task.query.filter_by(user_id=current_user.id).all()
            if current_user.is_authenticated
            else Task.query.all()
        )
        return render_template("task/task.html", form=form, tasks=tasks)


class TaskAddView(MethodView):
    def get(self):
        form = TaskForm()
        return render_template("task/add_task.html", form=form)

    def post(self):
        form = TaskForm()
        if form.validate_on_submit():
            task = Task(
                title=form.title.data,
                description=form.description.data,
                due_date=form.due_date.data,
                completed=form.completed.data,
                user_id=current_user.id if current_user.is_authenticated else None,
                status=form.status.data,
            )
            db.session.add(task)
            db.session.commit()
            return redirect(url_for("task.task"))
        return render_template("task/add_task.html", form=form)


# TODO: Update method post
class TaskEditView(MethodView):
    def get(self, id):
        task = Task.query.get_or_404(id)
        if not current_user.is_authenticated or task.user_id != current_user.id:
            flash("You are not allowed to edit this task.", "danger")
            return redirect(url_for("task.task"))
        form = TaskForm(obj=task)
        return render_template("task/edit_task.html", form=form)

    def post(self, id):
        task = Task.query.get_or_404(id)
        if not current_user.is_authenticated or task.user_id != current_user.id:
            flash("You are not allowed to edit this task.", "danger")
            return redirect(url_for("task.task"))
        form = TaskForm()
        if form.validate_on_submit():
            task.title = form.title.data
            task.description = form.description.data
            task.due_date = form.due_date.data
            task.completed = form.completed.data
            db.session.commit()
            return redirect(url_for("task.task"))
        return render_template("task/edit_task.html", form=form)


class TaskDeleteView(MethodView):
    def get(self, id):
        task = Task.query.get_or_404(id)
        if not current_user.is_authenticated or task.user_id != current_user.id:
            flash("You are not allowed to delete this task.", "danger")
            return redirect(url_for("task.task"))
        return render_template("task/delete_task.html", task=task)

    def post(self, id):
        task = Task.query.get_or_404(id)
        if not current_user.is_authenticated or task.user_id != current_user.id:
            flash("You are not allowed to delete this task.", "danger")
            return redirect(url_for("task.task"))
        db.session.delete(task)
        db.session.commit()
        flash("Task has been deleted.", "success")
        return redirect(url_for("task.task"))


class TaskUserListView(MethodView):
    def get(self, username):
        form = TaskForm()
        tasks = (
            Users.query.filter_by(username=username).first().tasks
            if current_user.is_authenticated
            else Task.query.all()
        )
        return render_template("task/task.html", form=form, tasks=tasks)


class TaskUserListCompletedView(MethodView):
    def get(self, username):
        form = TaskForm()
        tasks = (
            Task.query.filter_by(
                user_id=Users.query.filter_by(username=username).first().id,
                completed=True,
            )
            if current_user.is_authenticated
            else Task.query.all()
        )
        return render_template("task/task.html", form=form, tasks=tasks)


# NOTE: Task
task_bp.add_url_rule("/", view_func=TaskList.as_view("task"))
task_bp.add_url_rule("/add", view_func=TaskAddView.as_view("add"))
task_bp.add_url_rule("/edit/<int:id>", view_func=TaskEditView.as_view("edit"))
task_bp.add_url_rule("/delete/<int:id>", view_func=TaskDeleteView.as_view("delete"))

# NOTE: User tasks
task_bp.add_url_rule(
    "/user/<string:username>", view_func=TaskUserListView.as_view("user")
)

task_bp.add_url_rule(
    "/user/<string:username>/completed",
    view_func=TaskUserListCompletedView.as_view("user_completed"),
)
