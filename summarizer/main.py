import os
from dotenv import load_dotenv
from writer import Writer
from reader import DocumentsReader
from summarizer import Summarizer

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


for file_name in files_to_process:
    file_content = reader.get_file_content(filename=file_name)

    print(f"Generating summary for {file_content}")
    summary = summarizer.summarize(file_content)
    print(f"Summary of file {file_content}: \n {summary}")

    writer.save_to_file(path=f"documents/summarized/{file_name}.txt", content=summary)
