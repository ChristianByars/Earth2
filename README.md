# Earth2Studio Notebook

![Hurricane Florence Track Comparison](images/t2m_prediction.jpg)

AI weather forecasting using NVIDIA Earth2Studio on the SDSU SCIL Nautilus cluster.

## Prerequisites

- `kubectl` configured with access to the `sdsu-shen-climate-lab` namespace
- Python 3.12

## Kubernetes Setup

### Create Your Volume

Copy the volume template, then uncomment and set its name:

```bash
cp jupyter-volume.yaml jupyter-volume-<your-username>.yaml
sed -i 's/# name: jupyter-volume-{change name}/name: jupyter-volume-<your-username>/' jupyter-volume-<your-username>.yaml
```

Apply it:

```bash
kubectl create -f jupyter-volume-<your-username>.yaml -n <your-namespace>
```

### Create Your Pod

Copy the pod template, then set the deployment name and volume claim:

```bash
cp jupyter-pod-L40.yaml jupyter-pod-L40-<your-username>.yaml
sed -i \
  -e 's/jupyter-deployment-{user}/jupyter-deployment-<your-username>/' \
  -e 's/jupyter-volume-{user}/jupyter-volume-<your-username>/' \
  jupyter-pod-L40-<your-username>.yaml
```

Deploy:

```bash
kubectl create -f jupyter-pod-L40-<your-username>.yaml -n sdsu-shen-climate-lab
```

### Connect to JupyterLab

Get the Jupyter URL with token from the deployment logs:

```bash
kubectl logs deployment/jupyter-deployment-<your-username> -n sdsu-shen-climate-lab
```

Port forward (in a second terminal):

```bash
kubectl port-forward deployment/jupyter-deployment-<your-username> -n sdsu-shen-climate-lab 8888:8888
```

Open the `http://127.0.0.1:8888/lab?token=...` URL from the logs in your browser. If port 8888 is taken locally, use `8889:8888` and update the URL accordingly.

### Shutdown

```bash
kubectl delete -f jupyter-pod-L40-<your-username>.yaml -n sdsu-shen-climate-lab
```

Your volume persists across redeploys.

## Installation

Inside the JupyterLab terminal, install `curl` and `uv`:

```bash
sudo apt-get update && sudo apt-get install -y curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repo and install dependencies:

```bash
git clone https://github.com/ChristianByars/Earth2.git
cd Earth2
uv sync
```

Register the kernel:

```bash
uv run python -m ipykernel install --user --name earth2 --display-name "Earth2"
```

Open `Earth2.ipynb` and select the **"Earth2"** kernel.

## References

- [NVIDIA Earth2Studio](https://github.com/NVIDIA/earth2studio)
- [Earth2Studio Docs](https://nvidia.github.io/earth2studio/)
- [uv](https://docs.astral.sh/uv/)
- YouTube video link to my tutorial: https://www.youtube.com/watch?v=pEDuD49dReM
