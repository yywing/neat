package client

import (
	"fmt"
	"path"
	"strings"
)

func JoinURL(base string, paths ...string) string {
	p := path.Join(paths...)
	p = fmt.Sprintf("%s/%s", strings.TrimRight(base, "/"), strings.TrimLeft(p, "/"))
	if len(paths) > 0 && len(paths[len(paths)-1]) > 0 && paths[len(paths)-1][len(paths[len(paths)-1])-1] == '/' {
		return p + "/"
	}
	return p
}
