
from flask import Flask, render_template, request, redirect, url_for
import bleach

app = Flask(__name__)

# In-memory storage of notes as a list of dictionaries
notes = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']  # Retrieve title from form data
        note_content = request.form['note']
        # Sanitize the note content
        clean_note = bleach.clean(note_content, tags=['b', 'i', 'u', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'p', 'br', 'span'],
                                  attributes={'a': ['href', 'title', 'style'], 'p': ['style'], 'span': ['style']},
                                  strip=True)
        # Append both title and note to the notes list
        notes.append({'title': title, 'content': clean_note})
        return redirect(url_for('index'))
    return render_template('index.html', notes=notes)

@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    try:
        notes.pop(note_id)  # Remove the note by index
        return redirect(url_for('index'))
    except IndexError:
        return "Note not found", 404

if __name__ == '__main__':
    app.run(debug=True)
