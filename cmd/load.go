package cmd

import (
	"fmt"
	"log"
	"maps"
	"os"
	"path/filepath"
	"strings"

	"github.com/BurntSushi/toml"
	"github.com/spf13/cobra"
)

type Config map[string]any

var configPath string

var loadCmd = &cobra.Command{
	Use:   "load [profile]",
	Short: "Loads the environment profile (or default)",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		profile := "default"
		if len(args) > 0 {
			profile = args[0]
		}

		var config Config

		if _, err := toml.DecodeFile(configPath, &config); err != nil {
			log.Fatalf("Error reading TOML file: %v\n", err)
		}

		parts := strings.Split(profile, ".")
		envVars := resolveEnvVars(config, parts)
		for key, value := range envVars {
			fmt.Printf("export %s=\"%v\"\n", key, value)
		}
	},
}

func resolveEnvVars(config Config, profile []string) map[string]any {
	envVars := make(map[string]any)
	tables := make([]map[string]any, 0)

	for key, value := range config {
		if _, isTable := value.(map[string]any); !isTable {
			envVars[key] = value
			continue
		}

		if len(profile) > 0 && key == profile[0] {
			tables = append(tables, value.(map[string]any))
		}
	}

	// Keys in the subtable should take precedence over the ones in the main table.
	for _, value := range tables {
		maps.Copy(envVars, resolveEnvVars(value, profile[1:]))
	}

	return envVars
}

func resolveConfigPath(path string) string {
	if path != "" {
		return path
	}

	wd, err := os.Getwd()
	if err != nil {
		log.Fatalln("Error determining working directory:", err)
	}
	configPath := filepath.Join(wd, "dotem.toml")
	if _, err := os.Stat(configPath); err == nil {
		return configPath
	}

	homeDir, err := os.UserHomeDir()
	if err != nil {
		log.Fatalln("Error determining home directory:", err)
	}
	return filepath.Join(homeDir, "dotem.toml")
}

func init() {
	rootCmd.AddCommand(loadCmd)
	loadCmd.Flags().StringVarP(&configPath, "config", "c", "dotem.toml", "Path to the TOML configuration file")
}
