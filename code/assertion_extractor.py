#!/usr/bin/env python3
import os
import sys
import ast
import csv
import git
import tempfile
import logging
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class AssertionVisitor(ast.NodeVisitor):
    """AST visitor that finds all assertion statements in Python code."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.assertions = []
        self.current_class = None
        self.current_function = None
        self.line_mapping = {}
        
    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
        
    def visit_FunctionDef(self, node):
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
        
    def visit_Assert(self, node):
        line_num = node.lineno
        if line_num in self.line_mapping:
            assert_string = self.line_mapping[line_num]
        else:
            assert_string = f"Assert at line {line_num}"
            
        if self.current_function and (self.current_function.startswith('test_') or 
                                       self.current_function.startswith('Test') or 
                                       'test' in self.current_function.lower()):
            self.assertions.append({
                'filepath': self.filepath,
                'testclass': self.current_class or '',
                'testname': self.current_function,
                'line_number': line_num,
                'assert_string': assert_string.strip()
            })
        self.generic_visit(node)
        
    def visit_Call(self, node):
        # Check for assertEqual, assertTrue, etc. in test frameworks like unittest or pytest
        if isinstance(node.func, ast.Attribute) and node.func.attr.startswith(('assert', 'Assert')):
            line_num = node.lineno
            if line_num in self.line_mapping:
                assert_string = self.line_mapping[line_num]
            else:
                assert_string = f"Assertion method at line {line_num}"
                
            if self.current_function and (self.current_function.startswith('test_') or 
                                           self.current_function.startswith('Test') or 
                                           'test' in self.current_function.lower()):
                self.assertions.append({
                    'filepath': self.filepath,
                    'testclass': self.current_class or '',
                    'testname': self.current_function,
                    'line_number': line_num,
                    'assert_string': assert_string.strip()
                })
        self.generic_visit(node)

def build_line_mapping(file_path: str) -> Dict[int, str]:
    """Build a mapping from line numbers to line content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return {i+1: line for i, line in enumerate(f.readlines())}
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return {i+1: line for i, line in enumerate(f.readlines())}
        except Exception as e:
            logger.warning(f"Could not read file {file_path}: {str(e)}")
            return {}
    except Exception as e:
        logger.warning(f"Could not read file {file_path}: {str(e)}")
        return {}

def get_test_files(directory: str) -> List[str]:
    """Find all Python test files in a directory."""
    test_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and ('test' in file.lower() or 'test' in root.lower()):
                file_path = os.path.join(root, file)
                test_files.append(file_path)
    
    return test_files

def analyze_file(file_path: str) -> List[Dict]:
    """Analyze a Python file for assertions."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                file_content = file.read()
        except Exception as e:
            logger.warning(f"Could not read file {file_path}: {str(e)}")
            return []
    except Exception as e:
        logger.warning(f"Could not read file {file_path}: {str(e)}")
        return []
        
    try:
        tree = ast.parse(file_content)
        visitor = AssertionVisitor(file_path)
        visitor.line_mapping = build_line_mapping(file_path)
        visitor.visit(tree)
        return visitor.assertions
    except SyntaxError as e:
        logger.warning(f"Syntax error in {file_path}: {str(e)}")
        return []
    except Exception as e:
        logger.warning(f"Error analyzing {file_path}: {str(e)}")
        return []

def clone_github_repo(github_url: str) -> str:
    """Clone a GitHub repository and return the path to the cloned directory."""
    temp_dir = tempfile.mkdtemp()
    logger.info(f"Cloning {github_url} to {temp_dir}")
    
    try:
        git.Repo.clone_from(github_url, temp_dir)
        return temp_dir
    except git.GitCommandError as e:
        logger.error(f"Failed to clone repository: {str(e)}")
        sys.exit(1)

def write_assertions_to_csv(assertions: List[Dict], output_file: str):
    """Write assertions to a CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filepath', 'testclass', 'testname', 'line number', 'assert string'])
        
        for assertion in assertions:
            writer.writerow([
                assertion['filepath'],
                assertion['testclass'],
                assertion['testname'],
                assertion['line_number'],
                assertion['assert_string']
            ])

def extract_repo_name(github_url: str) -> str:
    """Extract repository name from GitHub URL."""
    if github_url.endswith('/'):
        github_url = github_url[:-1]
    return github_url.split('/')[-1]

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python assertion_extractor.py <github_url>")
        sys.exit(1)
        
    github_url = sys.argv[1]
    repo_name = extract_repo_name(github_url)
    output_file = f"{repo_name}_assertions.csv"
    
    # Clone the repository
    repo_dir = clone_github_repo(github_url)
    
    # Find all test files
    test_files = get_test_files(repo_dir)
    logger.info(f"Found {len(test_files)} test files")
    
    # Analyze each file
    all_assertions = []
    for file_path in test_files:
        logger.info(f"Analyzing {file_path}")
        file_assertions = analyze_file(file_path)
        all_assertions.extend(file_assertions)
    
    # Write results to CSV
    write_assertions_to_csv(all_assertions, output_file)
    logger.info(f"Found {len(all_assertions)} assertions in total")
    logger.info(f"Results written to {output_file}")

if __name__ == "__main__":
    main()