#!/usr/bin/env bash
# Build medcoupling from source against conda-provided deps.
# Usage: pixi run -e build _build-medcoupling
set -euo pipefail

MEDCOUPLING_VERSION="V9_14_0"
MEDCOUPLING_REPO="https://github.com/SalomePlatform/medcoupling.git"
CONFIG_URL="https://github.com/SalomePlatform/configuration/archive/refs/heads/master.tar.gz"

PREFIX="${CONDA_PREFIX:?run inside pixi}"
NCPU="$(sysctl -n hw.ncpu 2>/dev/null || nproc)"
WORKDIR="${TMPDIR:-/tmp}/medcoupling-build"
MEDCOUPLING_SRC="${WORKDIR}/medcoupling"
BUILD_DIR="${MEDCOUPLING_SRC}/build"

# OpenMPI wrapper hardcodes conda cross-compiler name; override to system clang
export OMPI_CC=clang
export OMPI_CXX=clang++

# ── clone / update source ────────────────────────────────────────────
if [ ! -d "${MEDCOUPLING_SRC}/.git" ]; then
    echo "==> cloning medcoupling ${MEDCOUPLING_VERSION}"
    mkdir -p "${WORKDIR}"
    git clone --branch "${MEDCOUPLING_VERSION}" --depth 1 \
        "${MEDCOUPLING_REPO}" "${MEDCOUPLING_SRC}"
else
    echo "==> resetting medcoupling to ${MEDCOUPLING_VERSION}"
    git -C "${MEDCOUPLING_SRC}" checkout -- .
    git -C "${MEDCOUPLING_SRC}" fetch --tags
    git -C "${MEDCOUPLING_SRC}" checkout "${MEDCOUPLING_VERSION}"
fi

# ── SALOME configuration cmake module ─────────────────────────────────
CFG_DIR="${MEDCOUPLING_SRC}/deps/config"
if [ ! -d "${CFG_DIR}/cmake" ]; then
    echo "==> fetching SALOME configuration module"
    mkdir -p "${CFG_DIR}"
    curl -fsSL "${CONFIG_URL}" | tar xz --strip-components=1 -C "${CFG_DIR}"
fi

# ── patch HDF5 cmake finder (from conda-forge feedstock) ──────────────
HDFCMAKE="${CFG_DIR}/cmake/FindSalomeHDF5.cmake"
if [ -f "${HDFCMAKE}" ] && ! grep -q "_first_hdf5_lib" "${HDFCMAKE}"; then
    echo "==> patching FindSalomeHDF5.cmake"
    python -c "
import pathlib
p = pathlib.Path('${HDFCMAKE}')
old = p.read_text()
new = old.replace(
    'GET_PROPERTY(_lib_lst SOURCE \${HDF5_LIBRARIES} PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG)',
    '''SET(_lib_lst \"\")
  LIST(GET HDF5_LIBRARIES 0 _first_hdf5_lib)
  IF(TARGET \${_first_hdf5_lib})
    GET_PROPERTY(_lib_lst TARGET \${_first_hdf5_lib} PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG)
  ENDIF()''')
p.write_text(new)
"
fi

# ── ensure python-config exists (SALOME cmake expects it) ─────────────
if [ ! -e "${PREFIX}/bin/python-config" ] && [ -e "${PREFIX}/bin/python3-config" ]; then
    ln -sf python3-config "${PREFIX}/bin/python-config"
fi

# ── ARM64 macOS: patch long vs long long ──────────────────────────────
# On ARM64, long and long long are both 64-bit but Clang treats them as
# incompatible types. libmed defines med_int as `long`. medcoupling uses
# int64_t (= long long) everywhere. We patch so the entire codebase
# consistently uses `long` for 64-bit integers.
ARM64_FLAGS=""
if [ "$(uname -m)" = "arm64" ]; then
    echo "==> patching int64_t types for ARM64 compatibility"

    sed -i.bak 's/typedef std::int64_t mcIdType;/typedef long mcIdType;  \/\/ ARM64: match med_int/' \
        "${MEDCOUPLING_SRC}/src/INTERP_KERNEL/MCIdType.hxx"

    sed -i.bak 's/using Int64 = std::int64_t;/using Int64 = long;  \/\/ ARM64: match med_int/' \
        "${MEDCOUPLING_SRC}/src/MEDCoupling/MCType.hxx"

    find "${MEDCOUPLING_SRC}/src" -name "*.cxx" -exec \
        sed -i.bak 's/std::int64_t/long/g' {} +

    # std::bind2nd removed in C++17
    sed -i.bak 's/std::bind2nd(std::not_equal_to<int>(),ref)/[ref](int v){ return v != ref; }/' \
        "${MEDCOUPLING_SRC}/src/ParaMEDMEM/InterpolationMatrix.cxx"

    find "${MEDCOUPLING_SRC}/src" -name "*.bak" -delete
    ARM64_FLAGS="-Wno-sign-conversion"
fi

# ── clean stale HEADERS (cause redefinition; must happen before configure) ─
# Only medcoupling installs .hxx/.txx/.i; libmed/HDF5 use .h
echo "==> cleaning stale medcoupling headers"
find "${PREFIX}/include" -maxdepth 1 \( -name "*.hxx" -o -name "*.txx" -o -name "*.i" \) -delete 2>/dev/null || true

# ── configure ─────────────────────────────────────────────────────────
rm -rf "${BUILD_DIR}"
echo "==> configuring in ${BUILD_DIR}"
cmake -B "${BUILD_DIR}" -S "${MEDCOUPLING_SRC}" \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="${PREFIX}" \
    -DPYTHON_ROOT_DIR="${PREFIX}" \
    -DPYTHON_EXECUTABLE="$(which python)" \
    -Wno-dev \
    -DCONFIGURATION_ROOT_DIR="${CFG_DIR}" \
    -DMED_INT_IS_LONG=ON \
    -DMEDCOUPLING_BUILD_TESTS=OFF \
    -DMEDCOUPLING_BUILD_PY_TESTS=OFF \
    -DMEDCOUPLING_BUILD_DOC=OFF \
    -DMEDCOUPLING_USE_64BIT_IDS=ON \
    -DMEDCOUPLING_ENABLE_PARTITIONER=OFF \
    -DMEDCOUPLING_ENABLE_RENUMBER=OFF \
    -DMEDCOUPLING_ENABLE_SHAPERECOGN=OFF \
    -DSALOME_USE_MPI=ON \
    -DMEDCOUPLING_USE_MPI=ON \
    -DMPI_C_COMPILER="$(which mpicc)" \
    -DMPI_CXX_COMPILER="$(which mpicxx)" \
    -DMEDCOUPLING_MEDLOADER_USE_XDR=OFF \
    -DXDR_INCLUDE_DIRS="" \
    -DCMAKE_CXX_FLAGS="${ARM64_FLAGS}" \
    -DCMAKE_SHARED_LINKER_FLAGS="-undefined dynamic_lookup" \
    -DCMAKE_MODULE_LINKER_FLAGS="-undefined dynamic_lookup"

# ── build + install ───────────────────────────────────────────────────
echo "==> building (${NCPU} cores)"
# build may return non-zero from optional SWIG targets; install anyway
cmake --build "${BUILD_DIR}" -j"${NCPU}" || true

# verify critical artifacts exist before installing
for lib in _medcoupling.so libmedcoupling.dylib libmedloader.dylib; do
    if ! find "${BUILD_DIR}" -name "${lib}" | grep -q .; then
        echo "FATAL: ${lib} not built" >&2; exit 1
    fi
done

echo "==> installing into ${PREFIX}"
# Disable rpath fixup — install_name_tool fails on already-fixed binaries
# and cmake treats it as fatal, aborting before later targets install.
cmake -DCMAKE_SKIP_INSTALL_RPATH=ON "${BUILD_DIR}" 2>/dev/null
cmake --install "${BUILD_DIR}"

# save manifest for clean uninstall on next rebuild
cp "${BUILD_DIR}/install_manifest.txt" "${WORKDIR}/install_manifest.txt" 2>/dev/null || true

echo "==> verifying"
python -c "import medcoupling; print('medcoupling OK')"

echo "==> running medconverter tests"
# skip: section tests need full SALOME; private/perf tests need EDF VPN
pytest test/test_simple.py test/test_aster.py test/test_backward_simple.py test/test_utilities.py \
    -x -q -n auto -k "not section"
