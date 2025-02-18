# myphoto_app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from .extensions import db
from .models import User, Photo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import threading
from .tasks import process_image

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        photo_data = file.read()
        new_photo = Photo(data=photo_data, owner_id=current_user.id)
        db.session.add(new_photo)
        db.session.commit()

        # Start background thread for processing the image
        thread = threading.Thread(target=process_image, args=(new_photo.id, current_user.id))
        thread.start()

        flash('Photo uploaded. Processing started.')
        return redirect(url_for('main.dashboard'))
    return render_template('upload.html')

@main.route('/dashboard')
@login_required
def dashboard():
    photos = Photo.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', photos=photos)
