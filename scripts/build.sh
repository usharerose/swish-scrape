#!/bin/bash
set -ex

# DESC: Usage help
# ARGS: None
# OUTS: None
function script_usage() {
  cat << EOF
Usage:
  -h|--help                  Displays this help
  -s|--service SERVICE_NAME  The name of service to set up in container
EOF
}

# DESC: Parameter parser
# ARGS: $@ (optional): Arguments provided to the script
# OUTS: Variables indicating command-line parameters and options
function parse_params() {
  local param
  while [[ $# -gt 0 ]]; do
    param="$1"
    shift
    case $param in
      -h | --help)
        script_usage
        exit 0
        ;;
      -s|--service )
        service_name=$1
        shift
        ;;
      *)
        script_usage
        exit 0
        ;;
    esac
  done
}

# DESC: Install python dependency defined in requirements.txt
# ARGS: None
# OUTS: None
function install_python_dependency() {
  # Upgrade pip
  pip install --upgrade pip
  # Install python dependency
  pip install --no-cache-dir -r /services/swish/${service_name}/requirements.txt
  # Clean python cache
  find /usr/local/ -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
}

# DESC: Actions following the security requirement
# ARGS: None
# OUTS: None
function security_requirement() {
  # Set permission
  chmod -R o-w /services/swish/${service_name}/
}

# DESC: Main control flow
# ARGS: $@ (optional): Arguments provided to the script
# OUTS: None
function main() {
  parse_params "$@"
  install_python_dependency
  security_requirement
}

# Make it rain
main "$@"
