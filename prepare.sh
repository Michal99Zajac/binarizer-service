#!/bin/sh

# Exit script with error if any step fails.
set -e

# Navigate to the project's git hooks directory.
cd .git/hooks

# Check if pre-commit file exists, if not, create it.
if [ ! -f pre-commit ]; then
    touch pre-commit
fi

# Make the pre-commit file executable.
chmod +x pre-commit

# Write the pre-commit actions into the file.
echo "#!/bin/sh
cargo fmt -- --check
cargo clippy -- -D warnings" > pre-commit

# Print a success message.
echo "Pre-commit hook has been installed."
