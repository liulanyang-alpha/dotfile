# codex_env

This directory contains the local wrapper scripts and runtime directories for
the isolated Codex environment.

- `install_codex_isolated.sh`: installs or updates nvm, Node.js LTS, and the
  Codex CLI inside `codex_env`.
- `start_codex.sh`: starts Codex with `CODEX_HOME` and `NVM_DIR` pointed at this
  isolated environment. Pass a directory as the first argument to choose the
  starting workspace.
- `vendor/nvm-install.sh`: vendored copy of the official nvm installer used by
  `install_codex_isolated.sh`.

`install_codex_isolated.sh` always treats its own directory as the environment
root. For example, if the installer is run from
`/opt/codex_env/install_codex_isolated.sh`, it will use:

- `/opt/codex_env/.codex` for `CODEX_HOME`
- `/opt/codex_env/.nvm` for `NVM_DIR`

This means the whole `codex_env` directory can be copied to another machine, and
the installer will keep `.codex` and `.nvm` inside that copied directory.

The actual nvm runtime files live in `.nvm`; do not edit those unless you are
intentionally updating nvm itself.
