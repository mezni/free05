uv init 
uv venv
source .venv/bin/activate
uv add --dev jupyterlab ipykernel
uv run jupyter lab
history