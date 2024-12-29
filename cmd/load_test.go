package cmd

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestResolveEnvVars(t *testing.T) {
	config := map[string]any{
		"key1": "value1",
		"key2": "value2",
		"default": map[string]any{
			"key3": "value3",
			"key4": "value4",
		},
		"profile1": map[string]any{
			"key5": "value5",
			"key6": "value6",
			"subprofile": map[string]any{
				"key6": "VALUE6",
				"key7": "value7",
			},
		},
		"profile2": map[string]any{
			"key8": "value8",
		},
	}

	testCases := []struct {
		in  string
		out map[string]string
	}{
		{"default", map[string]string{
			"key1": "value1",
			"key2": "value2",
			"key3": "value3",
			"key4": "value4",
		}},
		{"profile1", map[string]string{
			"key1": "value1",
			"key2": "value2",
			"key5": "value5",
			"key6": "value6",
		}},
		{"profile1.subprofile", map[string]string{
			"key1": "value1",
			"key2": "value2",
			"key5": "value5",
			"key6": "VALUE6",
			"key7": "value7",
		}},
		{"profile2", map[string]string{
			"key1": "value1",
			"key2": "value2",
			"key8": "value8",
		}},
	}

	for _, tc := range testCases {
		t.Run(tc.in, func(t *testing.T) {
			parts := strings.Split(tc.in, ".")
			envVars := resolveEnvVars(config, parts)
			assert.Equal(t, tc.out, envVars)
		})
	}
}

func TestResolveConfigPath(t *testing.T) {
	t.Run("CustomPath", func(t *testing.T) {
		path := resolveConfigPath("/custom/path/dotem.toml")
		assert.Equal(t, "/custom/path/dotem.toml", path)
	})

	t.Run("DefaultPathInCurrentDirectory", func(t *testing.T) {
		wd, _ := os.Getwd()
		filePath := filepath.Join(wd, "dotem.toml")
		_ = os.WriteFile(filePath, []byte(""), 0644)
		defer os.Remove(filePath)

		path := resolveConfigPath("")
		assert.Equal(t, filePath, path)
	})

	t.Run("DefaultPathInHomeDirectory", func(t *testing.T) {
		homeDir, _ := os.UserHomeDir()
		filePath := filepath.Join(homeDir, "dotem.toml")
		_ = os.WriteFile(filePath, []byte(""), 0644)
		defer os.Remove(filePath)

		path := resolveConfigPath("")
		assert.Equal(t, filePath, path)
	})
}

func TestLoadCmd(t *testing.T) {
	cmd := rootCmd

	t.Run("ValidConfigAndProfile", func(t *testing.T) {
		configContent := `
			key1 = "value1"

			[profile1]
			key2 = "value2"

			[profile1.profile2]
			key3 = "value3"
		`

		configFile := "dotem.toml"
		_ = os.WriteFile(configFile, []byte(configContent), 0644)
		defer os.Remove(configFile)

		args := []string{"load", "profile1.profile2"}
		cmd.SetArgs(args)

		output := new(bytes.Buffer)
		cmd.SetOut(output)
		cmd.SetErr(output)

		assert.NoError(t, cmd.Execute())

		outputStr := output.String()
		assert.Equal(t, outputStr, "export key1=\"value1\" key2=\"value2\" key3=\"value3\"")
	})
}
