import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Post, Comment, Report, SOSRequest, User
from anthropic import Anthropic

posts_bp = Blueprint('posts', __name__)

try:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY', 'your-api-key-here'))
except Exception as e:
    print(f"Anthropic initialization failed: {e}")
    client = None

@posts_bp.route('/')
def home():
    stats = {
        'total_posts': Post.query.count(),
        'total_users': User.query.count(),
        'safe_stories': Post.query.filter_by(is_anonymous=False).count()
    }
    return render_template('home.html', stats=stats)

@posts_bp.route('/dashboard')
@login_required
def dashboard():
    category = request.args.get('category')
    emotion = request.args.get('emotion')
    sort = request.args.get('sort', 'latest')

    query = Post.query.filter_by(is_flagged=False)

    if category:
        query = query.filter_by(category=category)
    if emotion:
        query = query.filter_by(emotion=emotion)

    if sort == 'latest':
        query = query.order_by(Post.created_at.desc())
    elif sort == 'liked':
        query = query.order_by(Post.likes_count.desc())

    posts = query.all()
    return render_template('dashboard.html', posts=posts)

@posts_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        # Rate Limiting: Max 5 posts per hour
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_posts_count = Post.query.filter(
            Post.user_id == current_user.id,
            Post.created_at >= one_hour_ago
        ).count()

        if recent_posts_count >= 5:
            flash('Rate limit exceeded. You can post a maximum of 5 thoughts per hour.', 'danger')
            return render_template('create_post.html')

        thought = request.form.get('thought')
        emotion = request.form.get('emotion')
        category = request.form.get('category')
        is_anonymous = request.form.get('is_anonymous') == 'on'

        new_post = Post(
            user_id=current_user.id,
            thought=thought,
            emotion=emotion,
            category=category,
            is_anonymous=is_anonymous
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Your thought has been shared safely.', 'success')
        return redirect(url_for('posts.dashboard'))

    return render_template('create_post.html')

@posts_bp.route('/api/ai-suggestion', methods=['POST'])
@login_required
def ai_suggestion():
    data = request.json
    thought = data.get('thought')
    
    if not thought or len(thought) < 10:
        return jsonify({'suggestion': ''})

    if not client:
        return jsonify({'suggestion': 'We are here for you. You are not alone in this journey. 💜'})

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            messages=[
                {"role": "user", "content": f"A woman shared this thought: {thought}. Give a 2-line warm, empathetic, supportive reply. Make her feel heard and not alone."}
            ]
        )
        suggestion = response.content[0].text
        return jsonify({'suggestion': suggestion})
    except Exception as e:
        print(f"Anthropic API Error: {e}")
        return jsonify({'suggestion': 'We are here for you. You are not alone in this journey. 💜'})

@posts_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.likes_count += 1
    db.session.commit()
    return jsonify({'success': True, 'count': post.likes_count})

@posts_bp.route('/post/<int:post_id>/report', methods=['POST'])
@login_required
def report_post(post_id):
    post = Post.query.get_or_404(post_id)
    reason = request.json.get('reason', 'General Report')
    
    # Check if user already reported this post
    existing_report = Report.query.filter_by(post_id=post_id, reported_by=current_user.id).first()
    if existing_report:
        return jsonify({'success': False, 'message': 'You have already reported this post.'})

    report = Report(post_id=post_id, reported_by=current_user.id, reason=reason)
    post.is_flagged = True # Auto-flag for admin review
    db.session.add(report)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Post reported successfully.'})

@posts_bp.route('/sos', methods=['POST'])
@login_required
def trigger_sos():
    message = request.form.get('message')
    sos = SOSRequest(user_id=current_user.id, message=message)
    db.session.add(sos)
    db.session.commit()
    return jsonify({'success': True, 'message': 'SOS request sent. Help is on the way.'})

@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    body = request.form.get('body')
    is_anonymous = request.form.get('is_anonymous') == 'on'

    if not body:
        return jsonify({'success': False, 'message': 'Comment body is required.'})

    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        body=body,
        is_anonymous=is_anonymous
    )
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'comment': {
            'username': 'Anonymous' if is_anonymous else current_user.username,
            'body': body,
            'created_at': comment.created_at.strftime('%b %d, %H:%M')
        }
    })

@posts_bp.route('/guidelines')
def guidelines():
    return render_template('safe_guidelines.html')
