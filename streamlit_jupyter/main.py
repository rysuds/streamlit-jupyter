import py
import sys
import typer
import nbformat
import asyncio
import subprocess


from copy import deepcopy
from subprocess import Popen, PIPE
from watchfiles import awatch, arun_process, run_process
from traitlets.config import Config
from nbconvert import PythonExporter
from nbconvert.exporters import export
from nbconvert.writers import FilesWriter
from nbconvert.preprocessors import Preprocessor
from typing import Optional
from streamlit import cli as stcli
from multiprocessing import Process



app = typer.Typer()

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
    print('---')
    python_exporter = StreamlitExporter()
    nb = nbformat.read(filename, as_version=4)
    output_tuple = export(python_exporter, nb=nb)
    writer = FilesWriter()
    output_name = filename.split('.ipynb')[0] if not output_name else output_name
    writer.write(*output_tuple, notebook_name=output_name)
    print('--**-')

# TODO pass args down?
# TODO async? https://github.com/tiangolo/typer/issues/88
# def watch_notebook(filename: str, output_name: Optional[str]) -> None:
#     async for _ in awatch(filename):
#         build_python_file(filename, output_name=output_name)

def run_streamlit(python_filename: str):
        sys.argv = ["streamlit", "run", python_filename]
        stcli.main()

async def watch_notebook(filename: str, output_name: Optional[str]):
    await arun_process(filename, target=build_python_file, args=(filename, output_name))


@app.callback()
def callback():
    """
    streamlit-jupyter: Streamlit for Jupyter Notebooks
    """


@app.command()
def run(filename: str):
    """
    Start Streamlit server from .ipynb file
    """
    if not filename.endswith('.ipynb'):
        typer.echo('Please only use with .ipynb files!')
        raise typer.Exit()
    else:
        output_name = filename.split('.ipynb')[0]
        python_filename = f"{output_name}.py"
        # run_process(filename, target=build_python_file, args=(filename, python_filename))
        p = Process(target=run_streamlit, args=(python_filename,))
        p.start()
        asyncio.run(watch_notebook(filename, output_name))
        # p.start()
        p.join()
        print('**')
        # subprocess.run(['streamlit', 'run', python_filename])
        # process = Popen(['streamlit', 'run', python_filename], stdout=PIPE, stderr=PIPE, shell=True)
        # stdout, stderr = process.communicate()

        # p = Process(target=run_streamlit, args=(python_filename,))

        # asyncio.run(watch_notebook(filename, python_filename))
        # print(stdout)
        # print('**')

