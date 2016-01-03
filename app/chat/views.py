from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask.ext.login import current_user, login_required
from app import app
from datetime import datetime
from app.lesson.models import Lesson

chat_bp = Blueprint('chat_bp', __name__, url_prefix='/chat')
socketio = SocketIO(app)


@chat_bp.route('/<lessonid>')
@login_required
def index(lessonid):
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found')
        return redirect(url_for('auth_bp.profile'))
    return render_template('chat/listing.html', lesson=lesson)


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count'],
          'hidden': 'true'})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    messages = [
        {'text': message['data'], 'sent': datetime.now().strftime('%H:%M %d-%m-%Y'), 'sender': current_user.first_name + ' ' + current_user.last_name}
    ]
    emit('my response',
         {'data': message['data'], 'count': session['receive_count'], 'messages': messages},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    # TODO: Add authentication
    messsages = [
        {'sender': 'Charles Thomas', 'text': 'Hello World', 'sent': datetime.now().strftime('%H:%M %d-%m-%Y')}
    ]
    emit('my response', {'data': 'Connected', 'count': 0, 'messages': messsages})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)