#!/bin/sh

export VENV_DIR='venv'

function _log() { echo "[$1] - $2" ; }
function _log_info() { _log "INFO" "$1" ; }
function _log_warn() { _log "WARN" "$1" ; }
function _log_error() { _log "ERROR" "$1" ; }

function _venv_install() {
    _log_info 'Creating Python virtual environment'
    python3 -m venv "${VENV_DIR}"
    if [ -z "${VIRTUAL_ENV}" ]; then
        source "${VENV_DIR}"/bin/activate
    fi
}

function _venv_check() {
    if [ -z "${VIRTUAL_ENV}" ]; then
        if [ ! -d "${VENV_DIR}" ]; then
            _venv_install
        fi
        _log_info "Activating Python virtual env with: $VENV_DIR/bin/activate"
        source "${VENV_DIR}"/bin/activate
    fi
}

function deps() {
    _log_header "Installing module dependencies"
    _venv_check
    python3 -m pip install -r requirements.txt
}

deps
