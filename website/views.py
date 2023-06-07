from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db # from the __init__.py file import db which is a SQLAlchemy object
import json

# factors applications to a blueprint to be called in __init__.py
views = Blueprint('views', __name__)

# routes to the home page (or root URL)
@views.route('/', methods=['GET', 'POST'])
@login_required  # decorator that mean you cannot see this page unless you're logged in
def home():
    # checks if new note is of appropriate length and then commits to the Note table.
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    # renders the home.html page after committing the note
    return render_template("home.html", user=current_user)

# if user presses 'delete' routes to /delete-note. Gets the noteId and deletes it
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:  # if a note is found
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})

# if user presses 'update' routes to /update-note/<int:note_id>/edit/ to update the note
@views.route('/update-note/<int:note_id>/edit/', methods=['GET', 'POST'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        updateNote = request.form.get('note')
        if len(updateNote) < 1:
            flash('Updated note is too short!', category='error')
        else:
            note.data = updateNote
            db.session.add(note)
            db.session.commit()
            flash('Note updated!', category='success')
            # returns to home.html after updating
            return redirect(url_for('views.home'))

    return render_template("update.html", user=note_id)
