# Building medcoupling on ARM64 macOS

## The problem

medcoupling's conda-forge feedstock has `skip: osx` — there are no prebuilt
packages for macOS. The underlying issue is a C++ type incompatibility between
libmed and medcoupling on ARM64.

## long vs long long on ARM64

On **x86_64 Linux**: `long` = 64 bits, `long long` = 64 bits.
Both map to the same underlying type. The compiler treats `long*` and
`long long*` as compatible.

On **ARM64 macOS**: `long` = 64 bits, `long long` = 64 bits.
Same size, but Clang treats them as **distinct, incompatible types**.
You cannot assign a `long*` to a `long long*` or vice versa.

## Where this bites

- **libmed** (the MED file I/O library) defines: `typedef long med_int;`
- **medcoupling** with `MEDCOUPLING_USE_64BIT_IDS=ON` defines:
  - `typedef std::int64_t mcIdType;` → `long long` on ARM64
  - `using Int64 = std::int64_t;` → `long long` on ARM64
- Every function that passes data between medcoupling and libmed
  hits `long*` vs `long long*` conversion errors.

With `64BIT_IDS=OFF`, `mcIdType = int32_t` (32-bit), which is too small
to hold libmed's 64-bit `med_int` values. So you can't just turn it off.

## The fix

The build script (`build-medcoupling.sh`) patches the source before building:

1. `MCIdType.hxx`: `typedef std::int64_t mcIdType` → `typedef long mcIdType`
2. `MCType.hxx`: `using Int64 = std::int64_t` → `using Int64 = long`
3. All `.cxx` files: `std::int64_t` → `long` (for any direct usage)

This makes all 64-bit integer types consistently `long`, matching libmed.
Since `long` is 64 bits on ARM64, no precision is lost.

Additional linker fix: `-undefined dynamic_lookup` is needed because Python
extensions on macOS resolve Python symbols at load time, not link time.

## SWIG typemap issue (64-bit IDs only)

Even with the `long` fix, SWIG-generated wrappers can have issues where
`std::vector<long>` and `std::vector<long long>` are treated as different
types. The `long` patching fixes this too since both sides now use `long`.
