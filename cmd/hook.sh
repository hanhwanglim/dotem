dotem() {
  if ! command -v dotem &> /dev/null; then
    echo "Error: dotem binary not found in PATH" >&2
    return 1
  fi

  eval "$(dotem "$@")"
  exit_code=$?

  if [ $exit_code -eq 0 ]; then
    eval "$output"
  else
    echo "$output" >&2
    return $exit_code
  fi
}
