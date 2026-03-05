from flask import Blueprint, render_template, request, make_response, jsonify, redirect, url_for
from ..models import Room, UserSession, Message, RoomMembership
from ..utils import generate_nick, generate_token
from .. import db
from config import Config

chat_bp = Blueprint('chat', __name__)


def _get_user(request):
    token = request.cookies.get('wr_token')
    if not token:
        token = generate_token()
    user = UserSession.get_or_create(token, generate_nick)
    return token, user


@chat_bp.route('/room/<room_name>')
def room(room_name):
    chat_room = Room.query.filter_by(name=room_name).first_or_404()
    token, user = _get_user(request)

    membership = RoomMembership.get(chat_room.id, user.id)

    messages = (
        chat_room.messages
        .order_by('created_at')
        .limit(Config.MESSAGE_HISTORY_LIMIT)
        .all()
    )

    # Get all members with roles
    members = (
        RoomMembership.query
        .filter_by(room_id=chat_room.id)
        .all()
    )

    resp = make_response(render_template(
        'chat/room.html',
        room=chat_room,
        history=messages,
        nick=user.nick,
        membership=membership,
        members=members,
        is_member=membership is not None,
        is_owner=membership.is_owner if membership else False,
    ))
    resp.set_cookie('wr_token', token, max_age=60*60*24*30)
    return resp


@chat_bp.route('/room/<room_name>/join', methods=['POST'])
def join_room_route(room_name):
    chat_room = Room.query.filter_by(name=room_name).first_or_404()
    token, user = _get_user(request)

    # Check if room already has an owner
    owner_exists = RoomMembership.query.filter_by(
        room_id=chat_room.id, role='owner'
    ).first()

    role = 'owner' if not owner_exists else 'member'
    RoomMembership.join(chat_room, user, role=role)

    resp = make_response(redirect(url_for('chat.room', room_name=room_name)))
    resp.set_cookie('wr_token', token, max_age=60*60*24*30)
    return resp


@chat_bp.route('/room/<room_name>/leave', methods=['POST'])
def leave_room_route(room_name):
    chat_room = Room.query.filter_by(name=room_name).first_or_404()
    token, user = _get_user(request)

    membership = RoomMembership.get(chat_room.id, user.id)
    if membership and membership.is_owner:
        # Transfer ownership to oldest member before leaving
        next_owner = (
            RoomMembership.query
            .filter_by(room_id=chat_room.id, role='member')
            .order_by(RoomMembership.joined_at)
            .first()
        )
        if next_owner:
            next_owner.role = 'owner'
            db.session.commit()

    RoomMembership.leave(chat_room, user)
    return redirect(url_for('main.index'))


@chat_bp.route('/room/<room_name>/remove/<int:member_id>', methods=['POST'])
def remove_member(room_name, member_id):
    chat_room = Room.query.filter_by(name=room_name).first_or_404()
    token, user = _get_user(request)

    # Only owner can remove
    my_membership = RoomMembership.get(chat_room.id, user.id)
    if not my_membership or not my_membership.is_owner:
        return jsonify({'error': 'Not authorized'}), 403

    target = RoomMembership.query.get(member_id)
    if target and target.room_id == chat_room.id and not target.is_owner:
        db.session.delete(target)
        db.session.commit()

    return redirect(url_for('chat.room', room_name=room_name))


@chat_bp.route('/room/<room_name>/promote/<int:member_id>', methods=['POST'])
def promote_member(room_name, member_id):
    chat_room = Room.query.filter_by(name=room_name).first_or_404()
    token, user = _get_user(request)

    my_membership = RoomMembership.get(chat_room.id, user.id)
    if not my_membership or not my_membership.is_owner:
        return jsonify({'error': 'Not authorized'}), 403

    target = RoomMembership.query.get(member_id)
    if target and target.room_id == chat_room.id:
        # Demote current owner to member
        my_membership.role = 'member'
        # Promote target to owner
        target.role = 'owner'
        db.session.commit()

    return redirect(url_for('chat.room', room_name=room_name))


@chat_bp.route('/room/<room_name>/search')
def search(room_name):
    chat_room = Room.query.filter_by(name=room_name).first_or_404()
    query = request.args.get('q', '').strip()
    if not query or len(query) < 2:
        return jsonify({'results': [], 'query': query, 'count': 0})
    results = Message.search(chat_room.id, query, limit=30)
    return jsonify({
        'query':   query,
        'count':   len(results),
        'results': [m.to_dict() for m in results],
    })
