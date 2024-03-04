package cmd

import (
	"github.com/spf13/cobra"
)

var Config string
var LoadAll bool

var loadCmd = &cobra.Command{
	Use:   "load",
	Short: "Loads the environment variables set in the profile",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		profile := "default"

		if LoadAll {
			profile = "ALL"
		} else if len(args) > 0 {
			profile = args[0]
		}

		if len(Config) > 0 {
			cmd.Println("loading profile", profile, "from", Config)
		} else {
			cmd.Println("loading profile", profile, "from default config")
		}
	},
}

func init() {
	rootCmd.AddCommand(loadCmd)

	loadCmd.Flags().BoolVarP(&LoadAll, "all", "", false, "Load all")
	loadCmd.Flags().StringVarP(&Config, "config", "", "", "Config file")
}
