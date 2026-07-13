#!/usr/bin/env bash

set -Eeuo pipefail

readonly APP_DIR="/root/benjamin-portfolio-site"
readonly SERVICE_NAME="myportfolio.service"
readonly VENV_DIR="${APP_DIR}/python3-virtualenv"
readonly HEALTH_URL="http://127.0.0.1:5000/timeline"
readonly LOCK_FILE="/tmp/benjamin-portfolio-redeploy.lock"

log() {
    printf '[redeploy] %s\n' "$*"
}

fail() {
    printf '[redeploy] ERROR: %s\n' "$*" >&2
    exit 1
}

for command_name in curl flock git systemctl; do
    command -v "${command_name}" >/dev/null 2>&1 || fail "Missing required command: ${command_name}"
done

[[ -d "${APP_DIR}/.git" ]] || fail "Git repository not found at ${APP_DIR}"
[[ -x "${VENV_DIR}/bin/python" ]] || fail "Python virtual environment not found at ${VENV_DIR}"
[[ -x "${VENV_DIR}/bin/pip" ]] || fail "pip not found in ${VENV_DIR}"
[[ -x "${VENV_DIR}/bin/flask" ]] || fail "Flask not found in ${VENV_DIR}"
[[ -f "${APP_DIR}/.env" ]] || fail "Missing ${APP_DIR}/.env"
systemctl cat "${SERVICE_NAME}" >/dev/null 2>&1 || fail "Missing systemd unit: ${SERVICE_NAME}"

exec 9>"${LOCK_FILE}"
flock -n 9 || fail "Another deployment is already running"

cd "${APP_DIR}"

current_branch="$(git branch --show-current)"
[[ "${current_branch}" == "main" ]] || fail "Expected branch main, found ${current_branch:-detached HEAD}"

working_tree_status="$(git status --porcelain)"
if [[ -n "${working_tree_status}" ]]; then
    printf '%s\n' "${working_tree_status}" >&2
    fail "Working tree is not clean; refusing to overwrite server changes"
fi

log "Fetching origin/main"
git fetch --prune origin main

read -r local_only remote_only < <(git rev-list --left-right --count HEAD...origin/main)
if (( local_only > 0 )); then
    fail "Server main has ${local_only} unpushed commit(s); refusing to deploy"
fi

if (( remote_only > 0 )); then
    log "Fast-forwarding main by ${remote_only} commit(s)"
else
    log "main is already current"
fi
git merge --ff-only origin/main

log "Installing Python dependencies"
"${VENV_DIR}/bin/pip" install --disable-pip-version-check -r requirements.txt

log "Running preflight checks"
"${VENV_DIR}/bin/python" -m compileall -q app tests
"${VENV_DIR}/bin/python" -m unittest discover -s tests
"${VENV_DIR}/bin/python" -c 'import app'

log "Restarting ${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

for attempt in $(seq 1 20); do
    if curl --fail --silent "${HEALTH_URL}" >/dev/null; then
        log "Deployment healthy at ${HEALTH_URL}"
        log "Running commit: $(git rev-parse --short HEAD)"
        exit 0
    fi

    if ! systemctl is-active --quiet "${SERVICE_NAME}"; then
        systemctl --no-pager --full status "${SERVICE_NAME}" >&2 || true
        fail "${SERVICE_NAME} exited during startup"
    fi

    sleep 1
done

systemctl --no-pager --full status "${SERVICE_NAME}" >&2 || true
journalctl --no-pager -u "${SERVICE_NAME}" -n 80 >&2 || true
fail "Health check did not pass within 20 seconds"
