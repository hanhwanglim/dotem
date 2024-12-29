package cmd

import (
	_ "embed"

	"github.com/spf13/cobra"
)

//go:embed hook.sh
var hook string

var hookCmd = &cobra.Command{
	Use:   "hook",
	Short: "Outputs a shell function to integrate into your shell",
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Println(hook)
	},
}

func init() {
	rootCmd.AddCommand(hookCmd)
}
