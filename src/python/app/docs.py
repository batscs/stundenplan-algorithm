import os
import markdown
import yaml
from jinja2 import Template

class DocumentationCompiler:
    def __init__(self, docs_folder, recompile=False):
        self.docs_folder = docs_folder
        self.template_path = os.path.join(docs_folder, "template.html")
        self.recompile = recompile
        self.compiled_docs = {}  # Cache to store compiled docs
        self.metadata = {}  # Cache to store metadata

    def load_metadata(self):
        """Load metadata.yml from the docs folder."""
        metadata_path = os.path.join(self.docs_folder, "metadata.yml")
        with open(metadata_path, "r") as f:
            return yaml.safe_load(f)

    def render_markdown(self, markdown_file):
        """Convert Markdown file to HTML."""
        md_path = os.path.join(self.docs_folder, markdown_file)
        with open(md_path, "r") as f:
            return markdown.markdown(f.read(), extensions=["fenced_code", "codehilite"])

    def get_all_markdown_files(self):
        """Get a list of all .md files in the docs folder, including subfolders."""
        md_files = []
        for root, dirs, files in os.walk(self.docs_folder):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.relpath(os.path.join(root, file), self.docs_folder))
        return md_files

    def compile(self):
        """Compile all documentation into HTML content."""
        # Recompile if requested or if cache is empty
        if self.recompile or not self.compiled_docs or not self.metadata:
            # Reload metadata
            self.metadata = self.load_metadata()

            with open(self.template_path, "r") as f:
                template = Template(f.read())

            # Compile all .md files
            for md_file in self.get_all_markdown_files():
                html_content = self.render_markdown(md_file)
                self.compiled_docs[md_file] = template.render(
                    title=self.metadata["title"],
                    sidebar=self.metadata["sidebar"],
                    content=html_content,
                )

        return self.compiled_docs

    def get_document(self, filename):
        """Get a compiled document by filename."""
        compiled_docs = self.compile()  # Ensure docs are compiled if not already
        md_filename = filename.replace(".html", ".md")
        if md_filename in compiled_docs:
            return compiled_docs[md_filename]
        return None
