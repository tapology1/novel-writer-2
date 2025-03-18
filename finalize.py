import sys
import json
import csv  # ✅ CSV module import

from writer import OpenAIWriter
from novel import *
from save import *
from settings import *
from misc import *

print("LLM Novel Writer - Finalizing")
print("----------------------------")

writer = OpenAIWriter(system_context)
novel_number, novel = load_or_create()

if hasattr(novel, "chapters") and novel.chapters:

    with open(f"novels/{novel_number}.txt", "w") as f_txt, \
         open(f"novels/{novel_number}.csv", "w", newline='', encoding='utf-8') as f_csv:  # ✅ Added CSV file

        csv_writer = csv.writer(f_csv)

        # ✅ Updated CSV header
        csv_writer.writerow(['Chapter Number', 'Title', 'Content', 'Polished'])

        # Write novel header to text file
        f_txt.write(f'{novel.title}\n\nBy AI written by Chase Adams\n\n')

        # ✅ Process chapters in numerical order
        for chapter_num in sorted(novel.chapters.keys(), key=lambda x: int(x)):
            chapter = novel.chapters[chapter_num]

            # Write to text file
            f_txt.write(f'Chapter {chapter_num}\n\n')

            # Collect content for CSV
            chapter_content = []
            for block_num in sorted(chapter.keys(), key=lambda x: int(x)):
                block_text = chapter[block_num]
                f_txt.write(f'{block_text}\n\n')
                chapter_content.append(block_text)

            # ✅ Write to CSV with the new "Polished" column set to False
            csv_writer.writerow([
                chapter_num,
                f'Chapter {chapter_num}',  # Preserve original title format
                '\n\n'.join(chapter_content),  # Match text file formatting
                "False"  # Polished column set to False
            ])

print(f"Text novel saved to novels/{novel_number}.txt")
print(f"CSV export saved to novels/{novel_number}.csv")
