# streamlit-jupyter
Generate Streamlit apps from a Jupyter notebook

[WORK IN PROGRESS!!]

## Installation
```
$ poetry install 
```

## Basic Usage

```
$ streamlit-jupyter run <.ipynb file>
```

This will launch a `watchfiles` process and a `streamlit` server. The watcher process will watch the `.ipynb` file for changes and trigger the creation of a `.py` file which will trigger the `streamlit` process to prompt a reload