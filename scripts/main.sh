#!/bin/bash
set -e

if [ -f scripts/pre-main.sh ]; then
    /bin/bash scripts/pre-main.sh || echo pre-main error
fi

# Procfile-prod is generated when building docker
exec honcho start --no-prefix -f Procfile-prod
