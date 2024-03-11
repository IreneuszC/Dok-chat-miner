import os
from dotenv import load_dotenv
from writer import Writer
from reader import DocumentsReader
from summarizer import Summarizer
from helpers import decorate_file_name

load_dotenv()
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

if OPEN_AI_KEY is None:
    print("OPEN_AI_API_KEY is required in .env file")
    exit()

writer = Writer()
reader = DocumentsReader()
summarizer = Summarizer(open_ai_api_key=OPEN_AI_KEY)

files_to_process = reader.get_files_to_process()

if len(files_to_process) == 0:
    print("No new files to summarize")
    exit()


# Create summary of each document
for group in files_to_process:
    print(f'Current group {group.get("name")}')
    for file_name in group.get("files"):
        print(f"Generating summary for {file_name}")
        file_content = reader.get_file_content(
            group_name=group.get("name"), file_name=file_name
        )
        summary = summarizer.summarize(file_content)

        writer.save_to_file(
            group_name=group.get("name"),
            file_name=decorate_file_name(file_name),
            content=summary,
        )


# Create summary of whole group
for group in files_to_process:
    group_name = group.get("name")
    summary_files = reader.get_summary_files(group_name=group_name)
    group_summary = ""

    for summary_file in summary_files:
        content = reader.get_file_content(group_name=group_name, file_name=summary_file)

        group_summary += content + "\n"

    print(f"Generating summary for group {group_name}")
    group_consistent_summary = summarizer.summarize(group_summary)
    writer.save_to_file(
        group_name=group_name, file_name="summary.txt", content=group_consistent_summary
    )
