import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def blah():
    """
    Run Streamlit from a Jupyter Notebook
    """
    typer.echo("Shooting portal gun")