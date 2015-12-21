from flask import Blueprint, render_template, flash, redirect, url_for, g
from flask.ext.login import login_required
from app.lesson.models import Lesson, LessonStudent
from .forms import AddStudyGroupForm, AddStudyGroupSessionForm
from .models import StudyGroup, StudyGroupMembers, StudyGroupSession
from datetime import datetime

studygroups_bp = Blueprint('studygroups_bp', __name__, url_prefix='/studygroups')


@studygroups_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    # TODO: Validate id
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found')
        return redirect(url_for('auth_bp.profile'))
    study_groups = [sg for sg in StudyGroup.select().where(StudyGroup.lesson == lessonid)]
    return render_template('studygroups/study_groups_listing.html', lesson=lesson, study_groups=study_groups)


@studygroups_bp.route('/add-studygroup', methods=('POST', 'GET'))
@login_required
def add_studygroup():
    form = AddStudyGroupForm()
    lesson_ids = [ls.lesson_id for ls in LessonStudent.select().where(LessonStudent.student_id == g.user.user_id)]
    if len(lesson_ids) < 1:
        flash("You do not have any lessons")
        return redirect(url_for("auth_bp.profile"))
    else:
        lessons = Lesson.select().where(Lesson.id << lesson_ids)
        form.lesson.choices = [(str(lesson.id), lesson.lesson_name) for lesson in lessons]

    if form.validate_on_submit():
        study_group = StudyGroup.create(
            location=form.location.data,
            lesson=form.lesson.data,
            founder=g.user.user_id
        )
        StudyGroupMembers.create(
            user=g.user.user_id,
            study_group=study_group
        )
        return redirect(url_for(".view", lessonid=form.lesson.data))
    return render_template('studygroups/add_studygroup.html', form=form)


@studygroups_bp.route('/add-session/<studygroupid>', methods=('POST', 'GET'))
@login_required
def add_studygroup_session(studygroupid):
    if not StudyGroup.select().where((StudyGroup.id == studygroupid) & (StudyGroup.founder == g.user.user_id)).exists():
        flash("Error! Invalid Study Group")
        return redirect(url_for("auth_bp.profile"))

    form = AddStudyGroupSessionForm()
    if form.validate_on_submit():
        dt = datetime.combine(form.date.data, form.time.data)
        StudyGroupSession.create(
            study_group=studygroupid,
            datetime=dt
        )
        return redirect(url_for("auth_bp.profile"))

    return render_template("studygroups/add_session.html", form=form)


@studygroups_bp.route('/detail/<sgid>')
@login_required
def detail(sgid):
    study_group = StudyGroup.get(StudyGroup.id == sgid)
    return render_template('studygroups/detail.html', study_group=study_group)


@studygroups_bp.route('/join/<sgid>')
@login_required
def join(sgid):
    try:
        sg = StudyGroup.get(StudyGroup.id == sgid)
    except:
        flash("Error. Invalid study group")
        return redirect(url_for(".detail", sgid=sgid))

    if sg.add_member(g.user):
        flash("Success")
    else:
        flash("Error")
    return redirect(url_for(".detail", sgid=sgid))


@studygroups_bp.route('/leave/<sgid>')
@login_required
def leave(sgid):
    try:
        sg = StudyGroup.get(StudyGroup.id == sgid)
    except:
        flash("Error. Invalid study group")
        return redirect(url_for(".detail", sgid=sgid))

    if sg.remove_member(g.user):
        flash("Success")
    else:
        flash("Error")
    return redirect(url_for(".detail", sgid=sgid))
