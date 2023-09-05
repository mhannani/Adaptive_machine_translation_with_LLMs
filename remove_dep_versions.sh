# Remove version information from each line in the temp file
awk -F'=' '{print $1}' requirements.txt > rm_versions_requirements.txt

echo "Requirements without dependency versions has been generated."