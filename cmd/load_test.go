package cmd

import (
	"bytes"
	"testing"
)

func TestLoadDefault(t *testing.T) {
	var output bytes.Buffer

	rootCmd.SetOut(&output)
	rootCmd.SetErr(&output)

	rootCmd.SetArgs([]string{"load"})
	rootCmd.Execute()

	expected := "export asdf"
	actual := output.String()

	if expected != actual {
		t.Fatalf(`Expected: %q  Got: %v`, expected, actual)
	}
}

func TestLoadDefaultWithConfig(t *testing.T) {
	var output bytes.Buffer

	rootCmd.SetOut(&output)
	rootCmd.SetErr(&output)

	rootCmd.SetArgs([]string{"load", "--config", "config-file"})
	rootCmd.Execute()

	expected := "export asdf"
	actual := output.String()

	if expected != actual {
		t.Fatalf(`Expected: %q  Got: %v`, expected, actual)
	}
}
