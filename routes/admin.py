from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, User, Post, Report, SOSRequest
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('posts.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.count(),
        'reports_count': Report.query.count(),
        'sos_count': SOSRequest.query.filter_by(is_resolved=False).count()
    }
    
    posts = Post.query.all()
    reports = Report.query.all()
    sos_requests = SOSRequest.query.filter_by(is_resolved=False).all()
    users = User.query.all()
    
    return render_template('admin_panel.html', 
                           stats=stats, 
                           posts=posts, 
                           reports=reports, 
                           sos_requests=sos_requests,
                           users=users)

@admin_bp.route('/admin/post/<int:post_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/sos/<int:sos_id>/resolve', methods=['POST'])
@login_required
@admin_required
def resolve_sos(sos_id):
    sos = SOSRequest.query.get_or_404(sos_id)
    sos.is_resolved = True
    db.session.commit()
    flash('SOS request marked as resolved.', 'success')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/user/<int:user_id>/ban', methods=['POST'])
@login_required
@admin_required
def ban_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Cannot ban an admin user.', 'danger')
    else:
        user.is_banned = True
        db.session.commit()
        flash(f'User {user.username} has been banned.', 'success')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/user/<int:user_id>/unban', methods=['POST'])
@login_required
@admin_required
def unban_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_banned = False
    db.session.commit()
    flash(f'User {user.username} has been unbanned.', 'success')
    return redirect(url_for('admin.admin_panel'))
