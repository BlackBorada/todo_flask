from flask import flash, render_template, redirect, url_for
from flask import Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Task
from app.forms import TaskForm

task_bp = Blueprint("task", __name__)


@task_bp.route("/")
def task():
    form = TaskForm()
    tasks = Task.query.filter_by(user_id=current_user.id).all() if current_user.is_authenticated else Task.query.all()  # noqa: E501
    return render_template("task/task.html", form=form, tasks=tasks)


@task_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            completed=form.completed.data,
            user_id = current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("task.task"))
    return render_template("task/add_task.html", form=form)


@task_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Task.query.get_or_404(id)
    if not current_user.is_authenticated or task.user_id != current_user.id :
        flash("You are not allowed to edit this task.", "danger")
        return redirect(url_for("task.task"))

    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.completed = form.completed.data
        db.session.commit()
        return redirect(url_for("task.task"))
    return render_template("task/edit_task.html", form=form)


@task_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    task = Task.query.get_or_404(id)
    if not current_user.is_authenticated or task.user_id != current_user.id:
        flash("You are not allowed to delete this task.",  "danger")
        return redirect(url_for("task.task"))

    db.session.delete(task)
    db.session.commit()
    flash("Task has been deleted.", "success")
    return redirect(url_for("task.task"))
