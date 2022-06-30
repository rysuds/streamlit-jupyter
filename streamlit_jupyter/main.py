import sys
import typer
import asyncio

from typing import Optional
from streamlit import cli as stcli
from multiprocessing import Process
from watchfiles import arun_process
from streamlit_jupyter.notebook import build_python_file

app = typer.Typer()

def run_streamlit(python_filename: str):
        sys.argv = ["streamlit", "run", python_filename]
        stcli.main()

# TODO pass args down?
# TODO async? https://github.com/tiangolo/typer/issues/88
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
    # TODO make it so that user can specify whether tehy want a specified python file, or whether they want temp dir?
    # like how Streamlit cli does it
    if not filename.endswith('.ipynb'):
        typer.echo('Please only use with .ipynb files!')
        raise typer.Exit()
    else:
        output_name = filename.split('.ipynb')[0]
        python_filename = f"{output_name}.py"

        # Build python file before streamlit runs
        build_python_file(filename, output_name)
        p = Process(target=run_streamlit, args=(python_filename,))
        p.start()
        asyncio.run(watch_notebook(filename, output_name))
        p.join()

