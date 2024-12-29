package cmd

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestHookCmd(t *testing.T) {
	cmd := rootCmd
	args := []string{"hook"}
	cmd.SetArgs(args)

	output := new(bytes.Buffer)
	cmd.SetOut(output)
	cmd.SetErr(output)

	assert.NoError(t, cmd.Execute())
	assert.Equal(t, output.String(), `dotem() {
  if ! command -v dotem &> /dev/null; then
    echo "Error: dotem binary not found in PATH" >&2
    return 1
  fi

  eval "$(dotem "$@")"
  exit_code=$?

  if [ $exit_code -eq 0 ]; then
    echo "$output"
  else
    echo "$output" >&2
    return $exit_code
  fi
}

`)
}
