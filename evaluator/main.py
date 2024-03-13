import evaluator as e
import os

evaluator = e.Evaluator()

path_to_directories = "../scrapper/output/clustering_results"
clustering_results_data = os.listdir(path_to_directories)
clustering_results_directories = [data for data in clustering_results_data if os.path.isdir(f"{path_to_directories}/{data}")]

print(f"\n1. Clustering results directories: ")
for directory, i in zip(clustering_results_directories, range(len(clustering_results_directories))):
    print(f"{i}. {str(directory)}")
    
for directory in clustering_results_directories:
    print(f"\nDirectory {directory}: ")
    path_to_directory = f"{path_to_directories}/{str(directory)}"
    content_of_directory = os.listdir(path_to_directory) # Names of directories
    print(f"Content of directory: {content_of_directory}")
    for inside_directory in content_of_directory:
        print(f"Files: ")
        path_to_inside_directory = f"{path_to_directory}/{str(inside_directory)}"
        content_of_inside_directory = os.listdir(path_to_inside_directory)
        print(content_of_inside_directory)
        for data in content_of_inside_directory:
            if not str(data).count("_summary") and not str(data).count("_score"):
                print(f"----{data}----")
                path_to_article_file = f"{path_to_inside_directory}/{data}"
                path_to_summary_file = path_to_article_file.replace(".txt", "_summary.txt")
                path_to_score_file = path_to_article_file.replace(".txt", "_score.txt")
                print(f"\nPath to article file: {path_to_article_file}")
                print(f"Path to summary file: {path_to_summary_file}")
                print(f"Path to score file: {path_to_score_file}\n")
                evaluator.evaluate_files(path_to_article_file, path_to_summary_file, path_to_score_file)