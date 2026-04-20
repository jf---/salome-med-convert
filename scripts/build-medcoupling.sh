#!/usr/bin/env bash
# Build medcoupling V9_14_0 from source with MPI + ARM64 patches.
set -euo pipefail

MEDCOUPLING_VERSION="V9_14_0"
PREFIX="${CONDA_PREFIX:?run inside pixi}"
NCPU="$(sysctl -n hw.ncpu 2>/dev/null || echo 4)"
SCRIPTDIR="$(cd "$(dirname "$0")" && pwd)"
BUILDROOT="$(cd "${SCRIPTDIR}/.." && pwd)/.build/medcoupling"
SRC_DIR="${BUILDROOT}/src"
CFG_DIR="${SRC_DIR}/deps/config"
BUILD_DIR="${SRC_DIR}/build"
SITEPKG="$(python -c 'import sysconfig; print(sysconfig.get_path("purelib"))')"

# ── skip if already installed ─────────────────────────────────────────
if python -c "import medcoupling; medcoupling.MEDCouplingUMesh" 2>/dev/null; then
    echo "medcoupling already installed, skipping (rm .build/medcoupling to force)"
    exit 0
fi

# OpenMPI wrappers hardcode conda cross-compiler; override to system clang
export OMPI_CC=clang OMPI_CXX=clang++ OMPI_FC="$(which gfortran)"

echo "==> building medcoupling ${MEDCOUPLING_VERSION}"

# ── clone source ──────────────────────────────────────────────────────
if [ ! -d "${SRC_DIR}/.git" ]; then
    mkdir -p "${BUILDROOT}"
    git clone --branch "${MEDCOUPLING_VERSION}" --depth 1 \
        https://github.com/SalomePlatform/medcoupling.git "${SRC_DIR}"
else
    git -C "${SRC_DIR}" checkout -- .
fi

# ── SALOME configuration cmake module ─────────────────────────────────
if [ ! -d "${CFG_DIR}/cmake" ]; then
    mkdir -p "${CFG_DIR}"
    curl -fsSL "https://github.com/SalomePlatform/configuration/archive/refs/tags/${MEDCOUPLING_VERSION}.tar.gz" \
        | tar xz --strip-components=1 -C "${CFG_DIR}"
fi

# ── patches ───────────────────────────────────────────────────────────
# HDF5 cmake finder (conda-forge feedstock)
HDFCMAKE="${CFG_DIR}/cmake/FindSalomeHDF5.cmake"
if ! grep -q "_first_hdf5_lib" "${HDFCMAKE}" 2>/dev/null; then
    python -c "
import pathlib
p = pathlib.Path('${HDFCMAKE}')
p.write_text(p.read_text().replace(
    'GET_PROPERTY(_lib_lst SOURCE \${HDF5_LIBRARIES} PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG)',
    'SET(_lib_lst \"\")\n  LIST(GET HDF5_LIBRARIES 0 _first_hdf5_lib)\n  IF(TARGET \${_first_hdf5_lib})\n    GET_PROPERTY(_lib_lst TARGET \${_first_hdf5_lib} PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG)\n  ENDIF()'))
"
fi

# python-config symlink (SALOME cmake expects it)
[ -e "${PREFIX}/bin/python-config" ] || ln -sf python3-config "${PREFIX}/bin/python-config"

# ARM64: long vs long long (see scripts/ARM64_BUILD_NOTES.md)
ARM64_FLAGS=""
if [ "$(uname -m)" = "arm64" ]; then
    echo "    patching for ARM64 (long vs long long, bind2nd)"
    sed -i.bak 's/typedef std::int64_t mcIdType;/typedef long mcIdType;/' \
        "${SRC_DIR}/src/INTERP_KERNEL/MCIdType.hxx"
    sed -i.bak 's/using Int64 = std::int64_t;/using Int64 = long;/' \
        "${SRC_DIR}/src/MEDCoupling/MCType.hxx"
    # medcoupling uses int64_t only as an alias for mcIdType, never for
    # wire-format integers, so this blanket replacement is safe.
    find "${SRC_DIR}/src" -name "*.cxx" -exec sed -i.bak 's/std::int64_t/long/g' {} +
    sed -i.bak 's/std::bind2nd(std::not_equal_to<int>(),ref)/[ref](int v){ return v != ref; }/' \
        "${SRC_DIR}/src/ParaMEDMEM/InterpolationMatrix.cxx"
    find "${SRC_DIR}/src" -name "*.bak" -delete
    ARM64_FLAGS="-Wno-sign-conversion"
fi

# clean stale headers from previous install (only medcoupling uses .hxx/.txx)
find "${PREFIX}/include" -maxdepth 1 \( -name "*.hxx" -o -name "*.txx" -o -name "*.i" \) -delete 2>/dev/null || true

# ── configure ─────────────────────────────────────────────────────────
rm -rf "${BUILD_DIR}"
cmake -B "${BUILD_DIR}" -S "${SRC_DIR}" \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="${PREFIX}" \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DPYTHON_ROOT_DIR="${PREFIX}" -DPYTHON_EXECUTABLE="$(which python)" \
    -DCONFIGURATION_ROOT_DIR="${CFG_DIR}" \
    -DMED_INT_IS_LONG=ON -DMEDCOUPLING_USE_64BIT_IDS=ON \
    -DMEDCOUPLING_BUILD_TESTS=OFF -DMEDCOUPLING_BUILD_PY_TESTS=OFF -DMEDCOUPLING_BUILD_DOC=OFF \
    -DMEDCOUPLING_ENABLE_PARTITIONER=OFF -DMEDCOUPLING_ENABLE_RENUMBER=OFF -DMEDCOUPLING_ENABLE_SHAPERECOGN=OFF \
    -DSALOME_USE_MPI=ON -DMEDCOUPLING_USE_MPI=ON \
    -DMPI_C_COMPILER="$(which mpicc)" -DMPI_CXX_COMPILER="$(which mpicxx)" \
    -DMEDCOUPLING_MEDLOADER_USE_XDR=OFF -DXDR_INCLUDE_DIRS="" \
    -DCMAKE_CXX_FLAGS="${ARM64_FLAGS}" \
    -DCMAKE_SHARED_LINKER_FLAGS="-undefined dynamic_lookup" \
    -DCMAKE_MODULE_LINKER_FLAGS="-undefined dynamic_lookup" \
    -Wno-dev

# ── build ─────────────────────────────────────────────────────────────
# ParaMEDMEM_Swig may fail on optional SWIG targets (warnings-as-errors);
# tolerate that only if the critical artifacts were produced.
BUILD_RC=0
cmake --build "${BUILD_DIR}" -j"${NCPU}" || BUILD_RC=$?

CRITICAL_LIBS="_medcoupling.so libmedcoupling.dylib libmedloader.dylib"
for lib in ${CRITICAL_LIBS}; do
    if ! find "${BUILD_DIR}" -name "${lib}" | grep -q .; then
        echo "FATAL: ${lib} not built (cmake exited ${BUILD_RC})" >&2; exit 1
    fi
done
if [ "${BUILD_RC}" -ne 0 ]; then
    echo "    build returned ${BUILD_RC} but critical artifacts present, continuing"
fi

# ── install ───────────────────────────────────────────────────────────
# strip install rules for files the build may not have produced —
# missing .pyc files and optional _ParaMEDMEM.so abort cmake --install
find "${BUILD_DIR}" -name "cmake_install.cmake" -exec \
    sed -i '' '/\.pyc"/d' {} +
if [ ! -f "${BUILD_DIR}/src/ParaMEDMEM_Swig/_ParaMEDMEM.so" ]; then
    : > "${BUILD_DIR}/src/ParaMEDMEM_Swig/cmake_install.cmake"
fi

cmake --install "${BUILD_DIR}"

# macOS case-insensitive FS: _MEDCoupling.so and _medcoupling.so share an
# inode. cmake installs _MEDCoupling.so first, clobbering _medcoupling.so.
# Force-copy the correct PyWrapping module (which bundles everything).
rm -f "${SITEPKG}/_MEDCoupling.so" "${SITEPKG}/_medcoupling.so"
cp "${BUILD_DIR}/src/PyWrapping/_medcoupling.so" "${SITEPKG}/_medcoupling.so"

# ── verify ────────────────────────────────────────────────────────────
python -c "import medcoupling; medcoupling.MEDCouplingUMesh" \
    || { echo "FATAL: medcoupling not importable after install" >&2; exit 1; }
echo "medcoupling OK"
