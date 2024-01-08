dotem() {
  result=$("dotem-cli" "$@")

  if [[ $result == "export "* || $result == "unset "* ]]; then
    eval "$result"
  else
    echo "$result"
  fi
}
