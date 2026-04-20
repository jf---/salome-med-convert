# Converter MED from/to other formats

Convert mesh files between MED and other FEA formats.

Supported formats: **SYSTUS**, **ABAQUS**, **ANSYS**, **Aster**, **ZSET**, **Tetgen**.

## Building (macOS ARM64)

All dependencies come from conda-forge via [pixi](https://pixi.sh). medcoupling and libmed-MPI are built from source (no conda packages for macOS).

```bash
pixi install
pixi run build
```

This builds libmed 4.2 with MPI, then medcoupling V9_14_0 with ARM64 `long`/`long long` patches. Both steps skip if already installed. Force rebuild with `rm -rf .build/`.

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
pixi run test
```

Tests requiring EDF VPN access (`test_private`, `test_perf`) or full SALOME (`section` tests) are excluded.
