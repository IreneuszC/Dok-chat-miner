import evaluator as e
import os

"""
Getting text from file.
"""
def get_text_from_file(path_to_file)->str:
    file = open(path_to_file, "r+")
    data = str(file.read())
    file.close()
    return data

"""
Writing text to file.
"""
def write_text_to_file(path_to_file, text)->None:
    file = open(path_to_file, "w+")
    file.write(text)
    file.close()

# 1. Creating the evaluator.
evaluator = e.Evaluator()

# 2. Setting path to output directories.
path_to_directories = "../scrapper/output/clustering_results"

# 3. Getting all directories in results.
clustering_results_data = os.listdir(path_to_directories)
clustering_results_directories = [data for data in clustering_results_data if os.path.isdir(f"{path_to_directories}/{data}")]

print(f"\n1. Clustering results directories: ")
for directory, i in zip(clustering_results_directories, range(len(clustering_results_directories))):
    print(f"{i}. {str(directory)}")
    
# 4. Iterating through every directory from algo method/ directory and doing evaluation.
for directory in clustering_results_directories:
    print(f"\nDirectory {directory}: ")
    path_to_directory = f"{path_to_directories}/{str(directory)}"
    content_of_directory = os.listdir(path_to_directory) # Names of directories
    print(f"Content of directory: {content_of_directory}")
    for inside_directory in content_of_directory:
        print(f"\n-------Directory: {inside_directory}--------\n")
        print(f"Files: ")
        path_to_inside_directory = f"{path_to_directory}/{str(inside_directory)}"
        content_of_inside_directory = os.listdir(path_to_inside_directory)
        print(content_of_inside_directory)
        data = "article_file, summary_file, score_file, bert score\n"
        report_file = open(f"{path_to_inside_directory}/raport.csv", "w+") # Opening the report file (.csv)
        
        # Iterating through every file in the directory.
        for file in content_of_inside_directory:
            if not str(file).count("_summary") and not str(file).count("_score") and not str(file).count("csv") and not str(file).count("summary"):
                print(f"----{file}----")
                path_to_article_file = f"{path_to_inside_directory}/{file}"
                path_to_summary_file = path_to_article_file.replace(".txt", "_summary.txt")
                path_to_score_file = path_to_article_file.replace(".txt", "_score.txt")
                name_of_article_file = file
                name_of_summary_file = name_of_article_file.replace(".txt", "_summary.txt")
                name_of_score_file = name_of_article_file.replace(".txt", "_score.txt")
                bert_score = evaluator.evaluate_files(path_to_article_file, path_to_summary_file, path_to_score_file) # Doing the evaluation,
                print(f"\nPath to article file: {path_to_article_file}")
                print(f"Path to summary file: {path_to_summary_file}")
                print(f"Path to score file: {path_to_score_file}")
                print(f"Bert score: {bert_score}\n")
                data += f"{name_of_article_file}, {name_of_summary_file}, {name_of_score_file}, {bert_score}\n"
        report_file.write(data)
        report_file.close() # Closing the csv file.