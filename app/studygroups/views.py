from flask import Blueprint, render_template, flash, redirect, url_for, g, request
from flask.ext.login import login_required
from app.lesson.models import Lesson, LessonStudent
from .forms import AddStudyGroupForm, AddStudyGroupSessionForm, ContactOrganiserForm, AddComment
from .models import StudyGroup, StudyGroupMembers, StudyGroupSession
from datetime import datetime, timedelta
import sendgrid
from app import sg
from app.auth.models import User

studygroups_bp = Blueprint('studygroups_bp', __name__, url_prefix='/studygroups')


@studygroups_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    """Route to display all the studygroups for a Lesson"""
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
    studygroup_session_form = AddStudyGroupSessionForm()
    return render_template('studygroups/study_groups_listing.html', lesson=lesson, study_groups=study_groups,
                           form=form, contact_form=contact_form, studygroup_session_form=studygroup_session_form)


@studygroups_bp.route('/add-studygroup', methods=('POST', 'GET'))
@login_required
def add_studygroup():
    """Route to either render the AddStudyGroupForm or to process it and create a new StudyGroup"""
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
    """Process the AddStudyGroupSessionForm and create a new StudyGroupSession via a POST request"""
    if not StudyGroup.select().where((StudyGroup.id == studygroupid) & (StudyGroup.founder == g.user.user_id)).exists():
        flash("Error! Invalid Study Group", 'error')
        return redirect(url_for("auth_bp.profile"))

    form = AddStudyGroupSessionForm()
    print('DATE')
    print(form.date.data)

    if form.validate_on_submit():
        dt = datetime.combine(form.date.data, form.time.data)
        s = StudyGroupSession.create(
            study_group=studygroupid,
            datetime=dt
        )
        print(s)
        if form.repeat.data is True:
            dt += timedelta(days=int(form.repeat_frequency.data))
            until = datetime.combine(form.repeat_until.data, datetime.min.time())
            while dt < until:
                s = StudyGroupSession.create(
                    study_group=studygroupid,
                    datetime=dt
                )
                dt += timedelta(days=int(form.repeat_frequency.data))

        flash("Success", 'success')
    return redirect(url_for(".detail",sgid=studygroupid))


@studygroups_bp.route('/detail/<sgid>')
@login_required
def detail(sgid):
    """Route to display the detail page for a StudyGroup"""
    study_group = StudyGroup.get(StudyGroup.id == sgid)
    comment_form = AddComment()
    comments = study_group.get_comments()
    studygroup_session_form = AddStudyGroupSessionForm()

    return render_template('studygroups/detail.html', study_group=study_group, comments=comments,
                           comment_form=comment_form, studygroup_session_form=studygroup_session_form)


@studygroups_bp.route('/join/<sgid>')
@login_required
def join(sgid):
    """Route to allow a user to join a StudyGroup"""
    # TODO: Move to POST request
    # TODO: Check if user already in StudyGroup
    try:
        sg = StudyGroup.get(StudyGroup.id == sgid)
    except:
        flash("Error. Invalid study group", 'error')
        return redirect(url_for(".detail", sgid=sgid))

    if sg.add_member(g.user):
        flash("Success", 'success')
    else:
        flash("Error", 'error')
    return redirect(url_for(".view", lessonid=sg.lesson.id))


@studygroups_bp.route('/leave/<sgid>')
@login_required
def leave(sgid):
    """Route to allow a user to leave a StudyGroup"""
    # TODO: Move to POST request
    # TODO: Check if user notalready in StudyGroup

    try:
        sg = StudyGroup.get(StudyGroup.id == sgid)
    except:
        flash("Error. Invalid study group", 'error')
        return redirect(url_for(".detail", sgid=sgid))

    if sg.remove_member(g.user):
        flash("Success", 'success')
    else:
        flash("Error", 'error')
    return redirect(url_for(".view", lessonid=sg.lesson.id))


@studygroups_bp.route('/add-comment/<sgid>', methods=('POST', 'GET'))
@login_required
def add_comment(sgid):
    """Route to process submission of the AddComment form via a POST request"""
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
    """Route to process the ContactOrganiserForm and send an email using the Sendgrid API"""
    # TODO: Check status of sent email
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
        flash('Success', 'success')

    return redirect(url_for(".view", lessonid=lessonid))


@studygroups_bp.route('/cancel<sessionid>')
@login_required
def cancel(sessionid):
    """Route to cancel a StudyGroupSession"""
    try:
        session = StudyGroupSession.get(StudyGroupSession.id == sessionid)
    except:
        flash("error", "Invalid Session")
        return redirect(url_for("auth_bp.profile"))
    print(session)
    if not session.study_group.founder.user_id == g.user.user_id:
        flash("Error! Invalid Study Group", 'error')
        return redirect(url_for("auth_bp.profile"))

    session.cancelled = True
    session.save()
    return redirect(url_for(".view", lessonid=session.study_group.lesson.id))