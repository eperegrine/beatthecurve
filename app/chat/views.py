from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask.ext.login import current_user, login_required
from app import app
from datetime import datetime
from app.lesson.models import Lesson, LessonStudent
from .models import Message
from app.models import r

chat_bp = Blueprint('chat_bp', __name__, url_prefix='/chat')
socketio = SocketIO(app)

clients = {}


@chat_bp.route('/<lessonid>')
@login_required
def index(lessonid):
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found', 'error')
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
    # TODO: Validate room
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    messages = [
        {
            'text': msg.text,
            'sent': msg.sent.strftime("%H:%M %d-%m-%Y"),
            'sender': msg.sender.first_name + ' ' + msg.sender.last_name
        }
        for msg in Message.select().where(Message.lesson == message['room']).order_by(Message.sent)
    ]
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count'],
          'messages': messages})
    '''clients[current_user.user_id][1] = message['room']
    active_users = {}
    for key,data in clients.items():
        if data[1] == message['room']:
            active_users[key] = clients[key]
    print(active_users)'''
    r.set(bytes(current_user.user_id), message['room'])
    r.rpush(message['room'], current_user.first_name + " " + current_user.last_name)
    emit('clients', {'clients': [str(name)[2:-1] for name in r.lrange(message['room'], 0, -1)]}, room=message['room'])


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
    print("leaving room")
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    messages = []
    try:
        msg = Message.create(
            text=message['data'],
            lesson=message['room'],
            sender=current_user.user_id,
        )
        messages.append({
            'text': msg.text,
            'sent': msg.sent.strftime("%H:%M %d-%m-%Y"),
            'sender': msg.sender.first_name + ' ' + msg.sender.last_name
        })
    except Exception as e:
        print(e)

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
    #clients[current_user.user_id] = [current_user.first_name + " " + current_user.last_name, '-1']
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    '''room = clients[current_user.user_id][1]
    clients.__delitem__(current_user.user_id)
    active_users = {}
    for key,data in clients.items():
        if data[1] == room:
            active_users[key] = clients[key]'''
    room = r.get(bytes(current_user.user_id))
    r.lrem(room, current_user.first_name + " " + current_user.last_name, 1)
    emit('clients', {'clients': [str(name) for name in r.lrange(room, 0, -1)]}, room=room)

    print('Client disconnected', request.sid)