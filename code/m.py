# import os
# import ast
# import csv
# from utils import TestVisitor

# def process_project(repo_url, output_csv):
#     # allows us to code the repo
#     repo_dir = "repo"
#     os.system(f"git clone {repo_url} {repo_dir}")

#     # open the csv
#     with open(output_csv, mode='w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["filepath", "testclass", "testname", "line number", "assert string"])

#         # traverse the directory python files
#         for root, _, files in os.walk(repo_dir):
#             for file in files:
#                 if file.endswith(".py"):
#                     filepath = os.path.join(root, file)
#                     try:
#                         with open(filepath, 'r', encoding='utf-8') as f:
#                             tree = ast.parse(f.read(), filename=filepath)
                        
#                         # ast visitor to extract test assertions
#                         visitor = TestVisitor(filepath)
#                         visitor.visit(tree)
#                         for entry in visitor.results:
#                             writer.writerow(entry)
#                     except Exception as e:
#                         print(f"Error processing {filepath}: {e}")

# if __name__ == "__main__":
#     repo_url = input("Enter GitHub repository URL: ")
#     output_csv = "output.csv"
#     process_project(repo_url, output_csv)