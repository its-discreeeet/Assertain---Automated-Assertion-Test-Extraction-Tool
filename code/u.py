# import ast

# class TestVisitor(ast.NodeVisitor):
#     def __init__(self, filepath):
#         self.filepath = filepath
#         self.results = []

#     def visit_ClassDef(self, node):
#         # Check if the class is a test class
#         is_test_class = any(
#             isinstance(base, ast.Attribute) and base.attr == "TestCase"
#             or isinstance(base, ast.Name) and base.id == "TestCase"
#             for base in node.bases
#         )
#         classname = node.name if is_test_class else ""
#         self.generic_visit(node)

#         # Visit methods within the class
#         for item in node.body:
#             if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
#                 self.process_test_function(classname, item)

#     def visit_FunctionDef(self, node):
#         # Handle standalone test functions
#         if node.name.startswith("test_"):
#             self.process_test_function("", node)
#         self.generic_visit(node)

#     def process_test_function(self, classname, node):
#         for stmt in node.body:
#             if isinstance(stmt, ast.Assert):
#                 self.results.append([
#                     self.filepath,
#                     classname,
#                     node.name,
#                     stmt.lineno,
#                     ast.unparse(stmt)
#                 ])
#             elif isinstance(stmt, ast.Call):
#                 # Handle self.assert* methods
#                 if isinstance(stmt.func, ast.Attribute) and stmt.func.attr.startswith("assert"):
#                     self.results.append([
#                         self.filepath,
#                         classname,
#                         node.name,
#                         stmt.lineno,
#                         ast.unparse(stmt)
#                     ])
