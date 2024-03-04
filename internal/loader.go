package internal

import (
	"fmt"
	"github.com/pelletier/go-toml"
	"os"
)

func LoadConfig(path string) (map[string]interface{}, error) {
	file, err := os.Open(path)

	if err != nil {
		return make(map[string]interface{}), err
	}

	defer file.Close()

	var config interface{}

	if err := toml.NewDecoder(file).Decode(&config); err != nil {
		return make(map[string]interface{}), err
	}

	data := config.(map[string]interface{})
	fmt.Println(data)
	return data, nil
}
