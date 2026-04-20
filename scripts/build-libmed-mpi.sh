#!/usr/bin/env bash
# Build libmed 4.2 with MPI from source.
# conda-forge only ships nompi builds for osx-arm64.
set -euo pipefail

VERSION="4.2"
PREFIX="${CONDA_PREFIX:?run inside pixi}"
NCPU="$(sysctl -n hw.ncpu 2>/dev/null || nproc)"
BUILDROOT="$(cd "$(dirname "$0")/.." && pwd)/.build/libmed"
SRC_DIR="${BUILDROOT}/med-copy-${VERSION}"

# ── skip if already installed with MPI ────────────────────────────────
if python -c "
import ctypes, pathlib
lib = pathlib.Path('${PREFIX}/lib/libmed.dylib')
if not lib.exists(): raise SystemExit(1)
ctypes.CDLL(str(lib)).MEDparFileOpen
" 2>/dev/null; then
    echo "libmed MPI already installed, skipping"
    exit 0
fi

# OpenMPI wrappers hardcode conda cross-compiler; override to system clang
export OMPI_CC=clang OMPI_CXX=clang++ OMPI_FC="$(which gfortran)"

echo "==> building libmed ${VERSION} (MPI)"

# ── fetch ─────────────────────────────────────────────────────────────
mkdir -p "${BUILDROOT}"
if [ ! -d "${SRC_DIR}" ]; then
    curl -fsSL "https://github.com/Krande/med-copy/archive/refs/tags/${VERSION}.tar.gz" \
        | tar xz -C "${BUILDROOT}"
fi

# ── remove nompi libmed (headers shadow MPI build) ────────────────────
if [ -f "${PREFIX}/include/medfile.h" ] && \
   ! nm "${PREFIX}/lib/libmed.dylib" 2>/dev/null | grep -q MEDparFileOpen; then
    echo "    removing nompi libmed"
    rm -f "${PREFIX}"/include/med*.h "${PREFIX}"/include/2.3.6/med*.h 2>/dev/null || true
    rm -f "${PREFIX}"/lib/libmed{,C,fwrap,import}*.dylib "${PREFIX}"/lib/libmed*.a 2>/dev/null || true
fi

# ── patch HDF5 version check (FATAL_ERROR on HDF5 2.x) ───────────────
MACROS="${SRC_DIR}/config/cmake_files/medMacros.cmake"
if grep -q "FATAL_ERROR.*HDF5 version" "${MACROS}" 2>/dev/null; then
    sed -i.bak 's/FATAL_ERROR\(.*HDF5 version\)/STATUS\1/g' "${MACROS}" && rm -f "${MACROS}.bak"
fi

# ── configure + build + install ───────────────────────────────────────
BUILD_DIR="${SRC_DIR}/build"
rm -rf "${BUILD_DIR}"
cmake -B "${BUILD_DIR}" -S "${SRC_DIR}" \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="${PREFIX}" \
    -DCMAKE_C_COMPILER="$(which mpicc)" -DCMAKE_CXX_COMPILER="$(which mpicxx)" \
    -DCMAKE_Fortran_COMPILER="$(which gfortran)" \
    -DMEDFILE_USE_MPI=ON -DMED_MEDINT_TYPE=long \
    -DMEDFILE_BUILD_TESTS=OFF -DMEDFILE_BUILD_PYTHON=OFF \
    -DHDF5_ROOT="${PREFIX}" \
    -DCMAKE_C_FLAGS="-DH5_USE_110_API" -DCMAKE_Fortran_FLAGS="-fdefault-integer-8" \
    -DCMAKE_SHARED_LINKER_FLAGS="-undefined dynamic_lookup" -Wno-dev

cmake --build "${BUILD_DIR}" -j"${NCPU}"
cmake --install "${BUILD_DIR}"

python -c "import ctypes; ctypes.CDLL('${PREFIX}/lib/libmed.dylib').MEDparFileOpen; print('libmed MPI OK')"
