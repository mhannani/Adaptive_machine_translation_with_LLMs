#!/bin/bash
pipdeptree --warn silence --freeze | grep -E '^\S' > requirements.txt

echo "Requirements file generated."