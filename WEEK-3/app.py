from flask import Flask, render_template, request, redirect

app = Flask(__name__)

notes = []

# Home Page
@app.route('/')
def home():
    search = request.args.get('search')

    if search:
        filtered_notes = [note for note in notes if search.lower() in note.lower()]
        return render_template('index.html', notes=filtered_notes)

    return render_template('index.html', notes=notes)


# Add Note
@app.route('/add', methods=['GET', 'POST'])
def add_note():

    if request.method == 'POST':
        note = request.form['note']
        notes.append(note)
        return redirect('/')

    return render_template('add_note.html')


# Edit Note
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):

    if id < 0 or id >= len(notes):
        return "Note not found"

    if request.method == 'POST':
        updated_note = request.form['note']
        notes[id] = updated_note
        return redirect('/')

    return render_template('edit_note.html', note=notes[id], id=id)

    if request.method == 'POST':
        updated_note = request.form['note']
        notes[id] = updated_note
        return redirect('/')

    return render_template('edit_note.html', note=notes[id], id=id)


# Delete Note
@app.route('/delete/<int:id>')
def delete_note(id):
    notes.pop(id)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)