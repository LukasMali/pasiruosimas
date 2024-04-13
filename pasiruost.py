from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Dictionary to hold users and their notes
user_notes = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def user_route():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            user_notes.setdefault(username, [])
            session['username'] = username
            return redirect(url_for('notes_route', username=username))
    return render_template('users.html', users=user_notes.keys())

@app.route('/delete_user/<username>', methods=['POST'])
def delete_user(username):
    user_notes.pop(username, None)  # Remove the user and their notes
    flash(f"User '{username}' and their notes have been deleted.")
    return redirect(url_for('user_route'))

@app.route('/notes/<username>', methods=['GET', 'POST'])
def notes_route(username):
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            user_notes[username].append(note)
    session['username'] = username
    return render_template('notes.html', notes=user_notes[username], username=username)

@app.route('/delete_note/<username>/<int:note_index>', methods=['POST'])
def delete_note(username, note_index):
    # Checks if the username is in the session and if the note_index is valid
    if 'username' in session and session['username'] == username:
        if username in user_notes and 0 <= note_index < len(user_notes[username]):
            user_notes[username].pop(note_index)  # Delete the note
            # Redirect to the notes page with a message indicating success
            flash('Note deleted successfully!')
        else:
            # Redirect to the notes page with an error message if the note doesn't exist
            flash('Note could not be found!')
    else:
        # Redirect to the login page with an error message if the user is not in session
        flash('You must be logged in to delete a note.')
    return redirect(url_for('notes_route', username=username))

if __name__ == '__main__':
    app.run(debug=True)
