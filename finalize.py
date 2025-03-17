import sys
import json

# Use 'pyreadline3' on Windows, 'readline' on Linux/macOS
if sys.platform == "win32":
    import pyreadline3 as readline
else:
    import readline

from writer import OpenAIWriter  # ✅ Using OpenAI instead of Anthropic
from novel import *
from save import *
from settings import *
from misc import *

print("LLM Novel Writer - Finalizing")
print("----------------------------")

# ✅ Use OpenAIWriter instead of AnthropicWriter
writer = OpenAIWriter(system_context)  

novel_number, novel = load_or_create()

# ✅ Ensure chapters exist before writing
if hasattr(novel, "chapters") and novel.chapters:
    with open(f"novels/{novel_number}.txt", "w") as f:
        # Write the title
        f.write(f'{novel.title}\n\nBy AI written by Chase Adams\n\n')

        for chapter_number, chapter_blocks in novel.chapters.items():
            # Write the chapter number
            f.write(f'Chapter {chapter_number}\n\n')

            # Write the chapter blocks
            for block_number, block_text in chapter_blocks.items():
                f.write(f'{block_text}\n\n')

print(f"Novel saved to novels/{novel_number}.txt")
