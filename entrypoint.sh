#!/bin/bash

# Install dependencies
pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

# Keep the container running
tail -f /dev/null
