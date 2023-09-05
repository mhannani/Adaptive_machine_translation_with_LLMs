#!/bin/bash
pipdeptree --warn silence --warn silence --freeze --warn silence | grep -E '^\S' > requirements.txt

echo "Requirements file generated."