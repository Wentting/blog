from flask_frozen import Freezer
from app import app
import os

freezer = Freezer(app)

@freezer.register_generator
def note():
    notes_dir = os.path.join(app.root_path, 'content', 'notes')
    for filename in os.listdir(notes_dir):
        if filename.endswith('.md'):
            yield {'note_id': filename.replace('.md', '')}

if __name__ == '__main__':
    freezer.freeze()