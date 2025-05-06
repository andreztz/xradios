# Default recipe: runs 'just --list'
default: list

# List all available recipes
list:
    @just --list

# Increments the version. Valid targets: major, minor, patch, pre_l, pre_n
bump target:
    bump-my-version bump {{ target }}

# Show the version after a bump with the given target.
bump-show target:
	bump-my-version show --increment {{ target }} new_version
 
# List all valid bump target
bump-show-all:
	bump-my-version show-bump

# Push current branch and tags to GitHub
deploy:
	git push --follow-tags
