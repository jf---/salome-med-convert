#!/usr/bin/env bash
# Build libmed 4.2 with MPI support from source.
# conda-forge only ships nompi builds for osx-arm64.
# Usage: pixi run -e build _build-libmed
set -euo pipefail

PREFIX="${CONDA_PREFIX:?run inside pixi}"
NCPU="$(sysctl -n hw.ncpu 2>/dev/null || nproc)"
WORKDIR="${TMPDIR:-/tmp}/libmed-mpi-build"
VERSION="4.2"

# ── skip if already built with MPI ────────────────────────────────────
if python -c "
import ctypes, pathlib
lib = pathlib.Path('${PREFIX}/lib/libmed.dylib')
if not lib.exists(): raise SystemExit(1)
ctypes.CDLL(str(lib)).MEDparFileOpen
" 2>/dev/null; then
    echo "==> libmed MPI already installed, skipping"
    exit 0
fi

# OpenMPI wrapper hardcodes arm64-apple-darwin20.0.0-clang which isn't
# on PATH during cmake build. Override to use system clang.
export OMPI_CC=clang
export OMPI_CXX=clang++
export OMPI_FC="$(which gfortran)"

echo "=== Building libmed ${VERSION} with MPI ==="

# ── fetch source ──────────────────────────────────────────────────────
mkdir -p "${WORKDIR}"
SRC_DIR="${WORKDIR}/med-copy-${VERSION}"
if [ ! -d "${SRC_DIR}" ]; then
    echo "==> downloading libmed ${VERSION}"
    curl -fsSL "https://github.com/Krande/med-copy/archive/refs/tags/${VERSION}.tar.gz" \
        | tar xz -C "${WORKDIR}"
fi

# ── remove nompi libmed from prefix (headers shadow MPI build) ────────
if [ -f "${PREFIX}/include/medfile.h" ] && \
   ! nm "${PREFIX}/lib/libmed.dylib" 2>/dev/null | grep -q MEDparFileOpen; then
    echo "==> removing nompi libmed (would shadow MPI headers)"
    rm -f "${PREFIX}"/include/med*.h 2>/dev/null || true
    rm -f "${PREFIX}"/include/2.3.6/med*.h 2>/dev/null || true
    rm -f "${PREFIX}"/lib/libmed*.dylib "${PREFIX}"/lib/libmed*.a 2>/dev/null || true
    rm -f "${PREFIX}"/lib/libmed*.11.* 2>/dev/null || true
fi

# ── patch HDF5 version check ─────────────────────────────────────────
# medMacros.cmake FATAL_ERRORs on HDF5 2.x (new versioning for 1.14+)
MACROS="${SRC_DIR}/config/cmake_files/medMacros.cmake"
if [ -f "${MACROS}" ] && grep -q "FATAL_ERROR.*HDF5 version" "${MACROS}"; then
    echo "==> patching medMacros.cmake HDF5 version check"
    sed -i.bak 's/FATAL_ERROR\(.*HDF5 version\)/STATUS\1/g' "${MACROS}"
    rm -f "${MACROS}.bak"
fi

# ── configure ─────────────────────────────────────────────────────────
BUILD_DIR="${SRC_DIR}/build-mpi"
rm -rf "${BUILD_DIR}"

echo "==> configuring (MPI=ON)"
cmake -B "${BUILD_DIR}" -S "${SRC_DIR}" \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="${PREFIX}" \
    -DCMAKE_C_COMPILER="$(which mpicc)" \
    -DCMAKE_CXX_COMPILER="$(which mpicxx)" \
    -DCMAKE_Fortran_COMPILER="$(which gfortran)" \
    -DMEDFILE_USE_MPI=ON \
    -DMED_MEDINT_TYPE=long \
    -DMEDFILE_BUILD_TESTS=OFF \
    -DMEDFILE_BUILD_PYTHON=OFF \
    -DHDF5_ROOT="${PREFIX}" \
    -DCMAKE_C_FLAGS="-DH5_USE_110_API" \
    -DCMAKE_Fortran_FLAGS="-fdefault-integer-8" \
    -DCMAKE_SHARED_LINKER_FLAGS="-undefined dynamic_lookup" \
    -Wno-dev

# ── build + install ───────────────────────────────────────────────────
echo "==> building (${NCPU} cores)"
cmake --build "${BUILD_DIR}" -j"${NCPU}"

echo "==> installing into ${PREFIX}"
cmake --install "${BUILD_DIR}"

# ── verify ────────────────────────────────────────────────────────────
echo "==> verifying MPI symbols"
python -c "
import ctypes
m = ctypes.CDLL('${PREFIX}/lib/libmed.dylib')
m.MEDparFileOpen
print('libmed MPI OK: MEDparFileOpen found')
"
