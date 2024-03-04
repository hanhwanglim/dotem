package testdata

import (
	"path/filepath"
	"runtime"
)

var basePath string

func init() {
	_, file, _, _ := runtime.Caller(0)
	basePath = filepath.Dir(file)
}

func Path(path string) string {
	return filepath.Join(basePath, path)
}
