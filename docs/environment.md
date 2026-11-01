# Environment notes

Tested on 31 October – 1 November 2026 on one NVIDIA L40 (48 GB), Python 3.12, with a CUDA 13 driver.

## Pinned stack

- earth2studio **0.20.0** (the version published on PyPI; uv resolves it through the PyPI and NVIDIA package indexes)
- torch **2.13.0** (CUDA 13.2 wheels from the `pytorch-cu132` index)
- All other versions are resolved in `uv.lock`; use `uv sync` (not `pip install`) so you get exactly the tested set.

## Install

```bash
uv sync
uv run python -m ipykernel install --user --name earth2 --display-name "earth2"
```

## Known issues and fixes

- **GPU memory between models.** Models from earlier cells stay on the GPU and can cause out-of-memory errors in later sections. Each notebook defines `free_gpu(...)` and calls it in a `finally:` block after every model, so it is released even when a cell fails. If a cell is interrupted by hand, restart the kernel.
- **`import cupy` needs pytest.** cupy imports `cupy.testing` internally, which requires `pytest`; it is listed in `dependencies` for that reason.
- **Headless runs.** `uv run jupyter nbconvert --to notebook --execute --allow-errors --inplace <notebook>` keeps the outputs of the cells that succeeded when a later cell fails.
- **Prebuilt torch-harmonics wheel.** torch-harmonics 0.8.1, which the `sfno` extra installs, is published on PyPI only as a source distribution and compiles CUDA extensions when it is installed; PyPI offers no prebuilt wheel of it for torch 2.13.0+cu132, so this repo expects one prebuilt cp312 wheel, `torch_harmonics-0.8.1-cp312-cp312-linux_x86_64.whl`, in a git-ignored `wheels/` folder at the repo root. `[tool.uv.sources]` points at it, and `uv sync` fails without it. Build it once against torch 2.13.0+cu132 following the upstream torch-harmonics build instructions, keep that exact file name, then run `uv lock`, because `uv.lock` pins the sha256 of the author's wheel. On the author's machine `wheels` is a symlink to a folder of prebuilt wheels. `pyproject.toml` also carries a flash-attn path source and override, but none of this repo's extras installs flash-attn (it is not in `uv.lock`), so they are inert here; if you add an extra that needs flash-attn, you must also supply a prebuilt `flash_attn-2.8.3-cp312-cp312-linux_x86_64.whl` in `wheels/`, because flash-attn is likewise published on PyPI only as a source distribution and needs a long CUDA compile.
- **CUDA 13 cupy and cucim.** The CUDA 13 builds (`cupy-cuda13x`, `cucim-cu13`) match torch 2.13.0+cu132. Importing earth2studio's models prints one harmless warning, `CuPy distance computation test failed with error: cuVS >= 24.12 or pylibraft < 24.12 should be installed to use this feature`; it only means the optional cuVS accelerator is not installed.
