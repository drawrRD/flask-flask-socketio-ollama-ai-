from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_socketio import leave_room, join_room

from config.extends import socketio
from practice01.decorators import login_required

bp = Blueprint('chatroom', __name__, url_prefix='/')

@bp.route('/chatroom', methods=['GET', 'POST'])
# @login_required
def chatroom_index():
    if request.method == 'GET':
        if 'username' in session:
            return redirect('/chat')
        return render_template('chatroom.html')
    else:
        username = request.form.get('username')
        room = request.form.get('room')
        session['username'] = username
        session['room'] = room
        return redirect('/chat')

@bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' in session and 'room' in session:
        username = session['username']
        room = session['room']
        return render_template('chat-begin.html', username=username, room=room)
    else:
        return redirect('/chatroom')

@bp.route('/chat/logout', methods=['GET'])
def chat_logout():
    del session['username']
    del session['room']
    return redirect('/chatroom')


online_user = []
room_user = {}


# # 连接
@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    online_user.append(username)
    print('connect info:  ' + f'{username}  已连接频道')
    print('online_user: ', online_user)
    socketio.emit('connect info', f'{username}  已连接频道')


# 断开连接
@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    print('connect info:  ' + f'{username}  断开连接')
    socketio.emit('connect info', f'{username}  断开连接')


# @socketio.on('connect info')
# def handle_connect_info(info):
#     print('connect info' + str(info))
#     room = session.get('room')
#     socketio.emit('connect info', info, to=room)


@socketio.on('send msg')
def handle_message(data):
    print('sendMsg' + str(data))
    room = session.get('room')
    data['message'] = data.get('message').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
    socketio.emit('show msg', data, to=room)


@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    try:
        room_user[room].append(username)
    except:
        room_user[room] = []
        room_user[room].append(username)

    join_room(room)
    print(username + ' 加入房间 ' + room + '\n')
    print(room_user)
    socketio.emit('connect info', username + ' 加入房间 ' + room, to=room)


@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    room_user[room].remove(username)
    leave_room(room)
    print(username + ' 离开房间 ' + room + '\n')
    print(room_user)
    socketio.emit('connect info', username + ' 离开房间 ' + room, to=room)


