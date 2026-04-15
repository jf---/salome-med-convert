# Converter MED from/to other formats

Convert mesh files between MED and other FEA formats.

Supported formats: **SYSTUS**, **ABAQUS**, **ANSYS**, **Aster**, **ZSET**, **Tetgen**.

Only meshes are converted for the moment. It is planned to also convert result fields.

## Building (macOS ARM64)

All dependencies come from conda-forge via [pixi](https://pixi.sh). medcoupling and libmed-MPI are built from source (no conda packages for macOS).

```bash
pixi install -e build
pixi run -e build bash scripts/build-libmed-mpi.sh
pixi run -e build bash scripts/build-medcoupling.sh
```

This builds libmed 4.2 with MPI, then medcoupling V9_14_0 with the ARM64 `long`/`long long` patches. The medcoupling script runs the test suite at the end (698 tests).

See `scripts/ARM64_BUILD_NOTES.md` for details on the ARM64 type compatibility issues.

## Usage

### Command line

```bash
medconverter run test/data/MOTIF_DONN1.ASC /tmp/motif.med
```

See `medconverter run --help` for available arguments.

### GUI

Standalone:

```bash
medconverter gui
```

As a SALOME plugin (requires SALOME 9.3+):

```bash
SALOME_PLUGINS_PATH=$(pwd) salome
```

## Testing

```bash
pixi run -e build pytest test/ -x -q -n auto -k "not section"
```

Tests requiring EDF VPN access (`test_private`, `test_perf`) or full SALOME (`section` tests) are excluded.

## Legacy installation (SALOME environment)

```bash
salome shell -- make
salome shell -- python test/run_unittest.py
```
