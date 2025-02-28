# myphoto_app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Photo
from . import db


views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('base.html')

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
        return redirect(url_for('main.dashboard'))
    return render_template('upload.html')

@views.route('/dashboard')
def dashboard():
    photos = Photo.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', photos=photos)
