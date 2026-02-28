from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .. import db
from ..models import Room, Message, UserSession

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ── Simple password protection ──────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


# ── Login ────────────────────────────────────────────────────────────────────
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        from flask import current_app
        password = request.form.get('password', '')
        if password == current_app.config.get('ADMIN_PASSWORD', 'admin1234'):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        error = 'Wrong password.'
    return render_template('admin/login.html', error=error)


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


# ── Dashboard ────────────────────────────────────────────────────────────────
@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'total_rooms':    Room.query.count(),
        'total_messages': Message.query.count(),
        'total_users':    UserSession.query.count(),
        'banned_users':   UserSession.query.filter_by(is_banned=True).count(),
    }
    rooms = Room.query.order_by(Room.created_at.desc()).all()
    return render_template('admin/dashboard.html', stats=stats, rooms=rooms)


# ── Rooms ────────────────────────────────────────────────────────────────────
@admin_bp.route('/rooms/<int:room_id>/delete', methods=['POST'])
@admin_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))


# ── Users ────────────────────────────────────────────────────────────────────
@admin_bp.route('/users')
@admin_required
def users():
    all_users = UserSession.query.order_by(UserSession.last_seen.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/<int:user_id>/ban', methods=['POST'])
@admin_required
def ban_user(user_id):
    user = UserSession.query.get_or_404(user_id)
    user.is_banned = True
    db.session.commit()
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/unban', methods=['POST'])
@admin_required
def unban_user(user_id):
    user = UserSession.query.get_or_404(user_id)
    user.is_banned = False
    db.session.commit()
    return redirect(url_for('admin.users'))
