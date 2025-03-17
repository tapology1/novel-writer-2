import sys
import json

# Use 'pyreadline3' on Windows, 'readline' on Linux/macOS
if sys.platform == "win32":
    import pyreadline3 as readline
else:
    import readline

# Import necessary modules
from novel import *
from save import *
from settings import *
from misc import *
from writer import OpenAIWriter  # Ensure the correct writer is imported

print("LLM Novel Writer - Outlining")
print("----------------------------")

# Initialize OpenAI writer using API key from settings
writer = OpenAIWriter()

# Load or create a novel
novel_number, novel = load_or_create()

# Function to safely call writer methods
def safe_writer_call(method, *args):
    try:
        return method(*args)
    except Exception as e:
        print(f"Error generating content: {e}")
        return ""

# Synopsis
if not getattr(novel, "synopsis", None):
    novel.setup()
    redo = True
    while redo:
        print(safe_writer_call(novel.create_synopsis, writer))
        redo = redo_prompt()
    novel_number = save_new(novel)

# Characters
if not getattr(novel, "characters", None):
    redo = True
    while redo:
        print(safe_writer_call(novel.create_characters, writer))
        redo = redo_prompt()
    save(novel, novel_number)

# Settings
if not getattr(novel, "settings", None):
    redo = True
    while redo:
        print(safe_writer_call(novel.create_settings, writer))
        redo = redo_prompt()
    save(novel, novel_number)

# Plot
if not getattr(novel, "plot", None):
    redo = True
    while redo:
        print(safe_writer_call(novel.create_plot, writer))
        redo = redo_prompt()
    save(novel, novel_number)

# Title
if not getattr(novel, "title", None):
    redo = True
    while redo:
        print(safe_writer_call(novel.create_title, writer))
        redo = redo_prompt()
    save(novel, novel_number)

print(f"This concludes the novel outlining process. You should now review the file at novels/{novel_number}.json and make edits as needed. After editing the file, run draft.py.")
