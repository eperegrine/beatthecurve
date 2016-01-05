from flask import Blueprint, render_template, flash, redirect, url_for, g, request
from flask.ext.login import login_required
from app.lesson.models import Lesson, LessonStudent
from .forms import AddStudyGroupForm, AddStudyGroupSessionForm, ContactOrganiserForm
from .models import StudyGroup, StudyGroupMembers, StudyGroupSession
from datetime import datetime
from .forms import AddComment
import sendgrid
from app import sg
from app.auth.models import User

studygroups_bp = Blueprint('studygroups_bp', __name__, url_prefix='/studygroups')


@studygroups_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    # TODO: Validate id
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found', 'error')
        return redirect(url_for('auth_bp.profile'))
    study_groups = [sg for sg in StudyGroup.select().where(StudyGroup.lesson == lessonid)]
    form = AddStudyGroupForm()
    lesson_ids = [ls.lesson_id for ls in LessonStudent.select().where(LessonStudent.student_id == g.user.user_id)]
    if len(lesson_ids) < 1:
        flash("You do not have any lessons", 'warning')
        return redirect(url_for("auth_bp.profile"))
    else:
        lessons = Lesson.select().where(Lesson.id << lesson_ids)
        form.lesson.choices = [(str(lesson.id), lesson.lesson_name) for lesson in lessons]
    contact_form = ContactOrganiserForm()
    return render_template('studygroups/study_groups_listing.html', lesson=lesson, study_groups=study_groups,
                           form=form, contact_form=contact_form)


@studygroups_bp.route('/add-studygroup', methods=('POST', 'GET'))
@login_required
def add_studygroup():
    form = AddStudyGroupForm()
    lesson_ids = [ls.lesson_id for ls in LessonStudent.select().where(LessonStudent.student_id == g.user.user_id)]
    if len(lesson_ids) < 1:
        flash("You do not have any lessons", 'warning')
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
        flash("Error! Invalid Study Group", 'error')
        return redirect(url_for("auth_bp.profile"))

    form = AddStudyGroupSessionForm()
    if form.validate_on_submit():
        dt = datetime.combine(form.date.data, form.time.data)
        StudyGroupSession.create(
            study_group=studygroupid,
            datetime=dt
        )
        flash("Success", 'success')
        return redirect(url_for(".detail",sgid=studygroupid))

    return render_template("studygroups/add_session.html", form=form)


@studygroups_bp.route('/detail/<sgid>')
@login_required
def detail(sgid):
    study_group = StudyGroup.get(StudyGroup.id == sgid)
    comment_form = AddComment()
    comments = study_group.get_comments()


    return render_template('studygroups/detail.html', study_group=study_group, comments=comments, comment_form=comment_form)


@studygroups_bp.route('/join/<sgid>')
@login_required
def join(sgid):
    try:
        sg = StudyGroup.get(StudyGroup.id == sgid)
    except:
        flash("Error. Invalid study group", 'error')
        return redirect(url_for(".detail", sgid=sgid))

    if sg.add_member(g.user):
        flash("Success", 'success')
    else:
        flash("Error", 'error')
    return redirect(url_for(".detail", sgid=sgid))


@studygroups_bp.route('/leave/<sgid>')
@login_required
def leave(sgid):
    try:
        sg = StudyGroup.get(StudyGroup.id == sgid)
    except:
        flash("Error. Invalid study group", 'error')
        return redirect(url_for(".detail", sgid=sgid))

    if sg.remove_member(g.user):
        flash("Success", 'success')
    else:
        flash("Error", 'error')
    return redirect(url_for(".detail", sgid=sgid))


@studygroups_bp.route('/add-comment/<sgid>', methods=('POST', 'GET'))
@login_required
def add_comment(sgid):
    comment_form = AddComment()
    study_group = StudyGroup.get(StudyGroup.id == sgid)

    if comment_form.validate_on_submit():
        if study_group.add_comment(comment_form.comment.data, user=g.user):
            flash("Success", 'success')
        else:
            flash("Error", 'error')
    return redirect(url_for(".detail", sgid=sgid))


@studygroups_bp.route('/contact-organiser/<lessonid>', methods=('POST', 'GET'))
@login_required
def contact_organiser(lessonid):
    form = ContactOrganiserForm(request.form)

    if form.validate_on_submit():
        message = sendgrid.Mail()
        studygroup = StudyGroup.get(StudyGroup.id == form.study_group.data)
        print(studygroup.founder.email)
        message.add_to(studygroup.founder.email)
        message.set_subject('Beat The Curve')
        message.set_text(form.message.data)
        message.set_from(g.user.email)
        status, msg = sg.send(message)
        print(status)
        flash('Success', 'success')

    return redirect(url_for(".view", lessonid=lessonid))