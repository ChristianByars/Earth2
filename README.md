# Earth2Studio Notebooks

AI weather forecasting using NVIDIA Earth2Studio on the SDSU SCIL Nautilus cluster.

## Prerequisites

- `kubectl` configured with access to the `sdsu-shen-climate-lab` namespace
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- Python 3.12

## Kubernetes Setup

### 1. Set Namespace Context

```bash
kubectl config set-context nautilus --namespace=sdsu-shen-climate-lab
```

### 2. Create Your Volume

Copy the volume template and replace `{user}` with your username:

```bash
cp jupyter-volume.yaml jupyter-volume-<your-username>.yaml
```

Edit `jupyter-volume-<your-username>.yaml` — uncomment and set the name on line 5:

```yaml
name: jupyter-volume-<your-username>
```

Apply it:

```bash
kubectl create -f jupyter-volume-<your-username>.yaml -n sdsu-shen-climate-lab
```

### 3. Create Your Pod

Copy the pod template and replace `{user}` with your username:

```bash
cp jupyter-pod-L40.yaml jupyter-pod-L40-<your-username>.yaml
```

Edit `jupyter-pod-L40-<your-username>.yaml`:

- **Line 5** — deployment name: `jupyter-deployment-<your-username>`
- **Line 62** — volume claim: `jupyter-volume-<your-username>`

Deploy:

```bash
kubectl create -f jupyter-pod-L40-<your-username>.yaml -n sdsu-shen-climate-lab
```

### 4. Connect to JupyterLab

Get your full pod name:

```bash
kubectl get pods -n sdsu-shen-climate-lab
```

Get the Jupyter URL with token:

```bash
kubectl logs <your-full-pod-name> -n sdsu-shen-climate-lab
```

Port forward (in a second terminal):

```bash
kubectl port-forward <your-full-pod-name> -n sdsu-shen-climate-lab 8888:8888
```

Open the `http://127.0.0.1:8888/lab?token=...` URL from the logs in your browser. If port 8888 is taken locally, use `8889:8888` and update the URL accordingly.

### 5. Shutdown

```bash
kubectl delete -f jupyter-pod-L40-<your-username>.yaml -n sdsu-shen-climate-lab
```

Your volume persists — your files will still be there next time you deploy.

## Installation

Inside the JupyterLab terminal:

```bash
git clone https://github.com/ChristianByars/Earth2.git
cd Earth2
uv sync
```

Register the kernel:

```bash
uv run python -m ipykernel install --user --name earth2 --display-name "Earth2 (Python 3.12)"
```

Select **"Earth2 (Python 3.12)"** as the kernel when running notebooks.

## Notebooks

| Notebook | Description |
|---|---|
| `Earth2.ipynb` | <!-- TODO: description --> |

## Sample Output

<!-- Add your images to the images/ folder and update the paths below -->

![TODO: caption](images/TODO.png)

![TODO: caption](images/TODO.png)


## References

- [NVIDIA Earth2Studio](https://github.com/NVIDIA/earth2studio)
- [Earth2Studio Docs](https://nvidia.github.io/earth2studio/)
- [uv](https://docs.astral.sh/uv/)