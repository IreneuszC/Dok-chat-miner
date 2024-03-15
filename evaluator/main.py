import evaluator as e
import os

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
        if not str(inside_directory).count("raport"):
            print(f"\n-------Directory: {inside_directory}--------\n")
            print(f"Files: ")
            path_to_inside_directory = f"{path_to_directory}/{str(inside_directory)}"
            content_of_inside_directory = os.listdir(path_to_inside_directory)
            print(content_of_inside_directory)
            data = "article_file, summary_file, reduced_summary_file, score_file, bert/cosine score, reduced bert/cosine score\n"
            report_file = open(f"{path_to_inside_directory}/raport.csv", "w+") # Opening the report file (.csv)
            total_score_file = open(f"{path_to_inside_directory}/total_score.txt", "w+") # Openning total bert score file (.txt)
            total_reduced_score_file = open(f"{path_to_inside_directory}/total_reduced_score.txt", "w+") # Openning total reduced bert score file (.txt)
            total_bert_score:float = 0
            total_reduced_bert_score:float = 0
            number_of_instances:float = 0
            # Iterating through every file in the directory.
            for file in content_of_inside_directory:
                if not str(file).count("_summary") and not str(file).count("_score") and not str(file).count("csv") and not str(file).count("summary"):
                    print(f"----{file}----")
                    
                    path_to_article_file = f"{path_to_inside_directory}/{file}"
                    path_to_summary_file = path_to_article_file.replace(".txt", "_summary.txt")
                    path_to_score_file = path_to_article_file.replace(".txt", "_score.txt")
                    path_to_reduced_summary_file = path_to_article_file.replace(".txt", "_reduced_summary.txt")
                    path_to_reduced_score_file = path_to_article_file.replace(".txt", "_reduced_score.txt")
                    
                    bert_score = evaluator.evaluate_files(path_to_article_file, path_to_summary_file, path_to_score_file) # Doing the evaluation,
                    reduced_bert_score = evaluator.evaluate_files(path_to_article_file, path_to_reduced_summary_file, path_to_reduced_score_file) # Doing the evaluation,
                    total_bert_score += bert_score
                    total_reduced_bert_score += reduced_bert_score
                    number_of_instances += 1
                    
                    name_of_article_file = file
                    name_of_summary_file = name_of_article_file.replace(".txt", "_summary.txt")
                    name_of_score_file = name_of_article_file.replace(".txt", "_score.txt")
                    name_of_reduced_summary_file = name_of_article_file.replace(".txt", "_reduced_summary.txt")
                    name_of_reduced_score_file = name_of_article_file.replace(".txt", "_reduced_score.txt")
                    
                    print(f"\nPath to article file: {path_to_article_file}")
                    print(f"Path to summary file: {path_to_summary_file}")
                    print(f"Path to reduced summary file: {path_to_reduced_summary_file}")
                    print(f"Path to score file: {path_to_score_file}")
                    print(f"Bert/cosine score: {bert_score}")
                    print(f"Reduced Bert/cosine score: {reduced_bert_score}\n")
                    data += f"{name_of_article_file}, {name_of_summary_file}, {name_of_reduced_summary_file}, {name_of_score_file}, {bert_score}, {reduced_bert_score}\n"
            report_file.write(data)
            report_file.close() # Closing the csv file.
            
            total_bert_score = total_bert_score / number_of_instances
            print(f"Total bert/cosine score: {total_bert_score}\n")
            total_score_file.write(str(total_bert_score))
            total_score_file.close() # Closing the total score file.
            
            total_reduced_bert_score = total_reduced_bert_score / number_of_instances
            print(f"Total reduced bert/cosine score: {total_reduced_bert_score}\n")
            total_reduced_score_file.write(str(total_reduced_bert_score))
            total_reduced_score_file.close() # Closing the total reduced score file.

# 5. Getting final raport.csv for each group
for directory in clustering_results_directories:
    print(f"\nDirectory {directory}: ")
    path_to_directory = f"{path_to_directories}/{str(directory)}"
    content_of_directory = os.listdir(path_to_directory) # Names of directories
    print(f"Content of directory: {content_of_directory}")
    raport_file = open(f"{path_to_directory}/raport.csv", "w+")
    data = "group, bert/cosine total score, bert/cosine reduced total score\n"
    for inside_directory in content_of_directory:
        if not str(inside_directory).count("raport") or str(inside_directory).count("score"):
            path_to_inside_directory = f"{path_to_directory}/{inside_directory}"
            path_to_total_score_file = f"{path_to_inside_directory}/total_score.txt"
            path_to_total_reduced_score_file = f"{path_to_inside_directory}/total_reduced_score.txt"
            total_score_file = open(path_to_total_score_file, "r+")
            reduced_total_score_file = open(path_to_total_reduced_score_file, "r+")
            total_score = total_score_file.read()
            reduced_total_score = reduced_total_score_file.read()
            total_score_file.close()
            reduced_total_score_file.close()
            result = f"{inside_directory}, {total_score}, {reduced_total_score}"
            print(f"Instance: {result}")
            data += f"{result}\n"
    raport_file.write(data)
    raport_file.close()