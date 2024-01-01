dotem() {
  result=$("dotem-cli" "$@")

  if [[ $result == "export "* ]]; then
    eval "$result"
  else
    echo "$result"
  fi
}
