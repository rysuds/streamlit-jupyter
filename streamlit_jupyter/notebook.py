import nbformat

from copy import deepcopy
from traitlets.config import Config
from nbconvert import PythonExporter
from nbconvert.exporters import export
from nbconvert.writers import FilesWriter
from nbconvert.preprocessors import Preprocessor

from typing import Optional


class StreamlitPreprocessor(Preprocessor):
    def preprocess_cell(self, cell, resources, cell_index):
        new_cell = deepcopy(cell)
        if cell.cell_type == 'markdown':
            new_cell.source = f"st.markdown('''{cell.source}''')"
            new_cell.cell_type = 'code'
            new_cell.outputs = list()
            new_cell.execution_count = None

        return new_cell, resources

class StreamlitExporter(PythonExporter):
    @property
    def default_config(self):
        c = Config()
        c.StreamlitExporter.preprocessors = [StreamlitPreprocessor]
        c.merge(super().default_config)
        return c

# TODO use tmp directory/file if specified?
def build_python_file(filename: str, output_name: Optional[str] ) -> None:
    nb = nbformat.read(filename, as_version=4)
    output_tuple = export(StreamlitExporter(), nb=nb)
    output_name = filename.split('.ipynb')[0] if not output_name else output_name
    FilesWriter().write(*output_tuple, notebook_name=output_name)