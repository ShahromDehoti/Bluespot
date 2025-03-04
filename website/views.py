# myphoto_app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Photo
from . import db
from flask_login import login_required, current_user
import base64

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return render_template('index.html')

@views.route('/upload', methods=['GET', 'POST'])
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

        flash('Photo uploaded. Processing started.')
        return redirect(url_for('views.dashboard'))
    return render_template('upload.html', user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    photos = Photo.query.filter_by(owner_id=current_user.id).all()
    # Convert binary photo data to base64 for display
    photo_data = []
    for photo in photos:
        encoded_data = base64.b64encode(photo.data).decode('utf-8')
        photo_data.append({
            'id': photo.id,
            'data': encoded_data,
            'description': photo.description,
            'upload_date': photo.upload_date
        })
    return render_template('dashboard.html', photos=photo_data)
