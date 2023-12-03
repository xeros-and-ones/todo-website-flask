from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_text = request.form.get('note')

        if len(note_text) < 2:
            flash('Note is too short', category='danger')
        else:
            new_note = Note(todo_note=note_text, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home.html", user=current_user)


@views.route('/api')
def api():
    return render_template("api.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return None
