# AGENTS.md

fish-shell is a hybrid C+Rust project. Rust (`src/`, `crates/*`) is the primary
language; C is a small shim (see `build.rs`). CMake wraps Cargo, so most dev
workflows go through CMake/make rather than raw `cargo`.

## Build

- CMake is the real build frontend; `GNUmakefile` is a thin wrapper around it.
  Standard flow: `mkdir build && cd build && cmake .. && make` (or `make fish_run_tests`).
  The build produces `build/fish` plus `fish_indent`/`fish_key_reader` symlinks.
- `cargo build --bin fish` also works for fast Rust-only iteration; `build.rs`
  embeds the `share/` runtime dir via `rust-embed` and resolves canonical paths,
  so the binary runs straight out of the build dir without installing.
- Rust toolchain: edition 2024, MSRV pinned at **1.85**; CI also tests on stable (1.98).
  Both are pinned in `.github/actions/rust-toolchain/action.yml` (see `updatecli.d/rust.yml`).
- Feature flags matter: default features = `embed-manpages,localize-messages`. CI builds
  and clippys under default, `--no-default-features`, and `--all-features`; keep all three working.

## Tests

- `tests/test_driver.py` is the integration runner. It drives:
  - `tests/checks/*.fish` via `littlecheck.py` (scripted shell tests),
  - `tests/pexpects/*.py` via `pexpect` (interactive-terminal tests).
- Run everything: `make -C build fish_run_tests` (CI does `env CI=1 ninja fish_run_tests`).
- Run one check: `tests/test_driver.py build checks/<name>.fish` (from repo root);
  individual CMake targets `test_<name>.fish` exist too they need the binaries built first.
- The test driver sets a sandboxed `$HOME` and uses `FISH_TEST_MAX_CONCURRENCY`
  (CI sets it to 4) to bound parallel tests.
- Rust unit/doc tests: `cargo test` / `cargo test --doc`.

## Checks (lint gate)

- `cargo xtask check` runs `build_tools/check.sh` — the full gate CI uses:
  build, `shellcheck`, `cargo xtask format --all --check`, clippy across the three
  feature sets, gettext/fluent extraction checks, `cargo test`, rustdoc.
  Set `FISH_CHECK_LINT=false` to skip the lint half (Windows CI does this).
- Individual lint jobs (see `.github/workflows/lint.yml`):
  - `cargo xtask format --all --check` (needs a `fish_indent` binary on `PATH`).
  - `rustfmt --check` over all `*.rs` in `build.rs crates src`.
  - clippy: `cargo clippy --workspace --all-targets -- --deny=warnings`; `clippy.toml`
    forbids direct `libc::setlocale` (use `src/locale.rs` wrappers).
  - rustdoc: `RUSTDOCFLAGS='-D warnings' cargo doc --workspace`.
  - The lint CI also checks an import convention: `nix::unistd::Pid` must be imported
    as `NullablePid` (`git grep` fails on bare `unistd::Pid`).

## Conventions

- The project is heavily documented in `CONTRIBUTING.rst` (dev setup, code style,
  testing) and `README.rst` — read `CONTRIBUTING.rst` before making non-trivial changes.
- `CHANGELOG.rst` is kept up to date per release; note the project style for changes.
- Completions for external tools live under `share/completions/*.fish`.
- `crates/` are internal workspace libs (gettext, localization, wide strings, etc.);
  keep crates loosely coupled and no cross-crate `src/` imports.
- Generated/locale files: gettext/fluent extraction is done via `cargo xtask gettext`
  and `cargo xtask fluent`; keep PO/FTL files in sync (CI enforces this).