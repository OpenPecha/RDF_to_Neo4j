import os
import sys

# Ensure both the src/ root and the package directory are importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
PKG_DIR = os.path.join(SRC_DIR, "RDF_to_Neo4j")

for path in (SRC_DIR, PKG_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)


