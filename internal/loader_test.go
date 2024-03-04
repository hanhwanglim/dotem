package internal

import (
	"fmt"
	"github.com/hanhwanglim/dotem/testdata"
	"testing"
)

func TestLoader(t *testing.T) {
	data, err := LoadConfig(testdata.Path("data.toml"))

	if err != nil {
		t.Fatalf("Error: %q this ", err)
	}

	for key, value := range data {
		fmt.Println("Key: ", key, "; Value: ", value)
	}

}
