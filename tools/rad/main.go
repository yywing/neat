package main

import (
	"bytes"
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httputil"
	"os"
	"strconv"
	"sync"
	"time"

	"github.com/spf13/cobra"
	client "github.com/yywing/neat/client/neat-client-go"
)

var (
	name       = "rad-tools"
	version    = "0.0.1"
	githash    = "undefined"
	buildstamp = "undefined"
	filePath   = ""
	url        = ""
)

type RadOutput struct {
	Method string
	URL    string
	Header map[string]string
	Body   []byte `json:"b64_body,omitempty"`
}

func (r *RadOutput) ToRequest() (*http.Request, error) {
	body := bytes.NewReader(r.Body)
	return http.NewRequest(r.Method, r.URL, body)
}

func send(r *RadOutput) {
	req, err := r.ToRequest()
	if err != nil {
		log.Printf("[%v] %v to request error: %v.", r.Method, r.URL, err)
		return
	}
	rawRequest, err := httputil.DumpRequestOut(req, true)
	if err != nil {
		log.Printf("[%v] %v get raw request error: %v.", r.Method, r.URL, err)
		return
	}
	portStr := req.URL.Port()
	scheme := client.Scheme(req.URL.Scheme)
	if portStr == "" {
		if scheme == client.HTTP {
			portStr = "80"
		}
		if scheme == client.HTTPS {
			portStr = "443"
		}
	}
	port, err := strconv.Atoi(portStr)
	if err != nil {
		log.Printf("[%v] %v get port error: %v.", r.Method, r.URL, err)
		return
	}
	c := &http.Client{}
	neatClient := client.NewNeatClient(url, c)
	neatReq := &client.CreateRawRequest{
		RawRequest: base64.StdEncoding.EncodeToString(rawRequest),
		Scheme:     client.Scheme(req.URL.Scheme),
		Host:       req.Host,
		Port:       uint16(port),
	}
	ctx := context.Background()
	_, err = neatClient.CreateRaw(ctx, client.DefaultHeader, neatReq)
	if err != nil {
		log.Printf("[%v] %v request neat error: %v", r.Method, r.URL, err)
		return
	}
	log.Printf("[%v] %v request neat success", r.Method, r.URL)
}

func load(cmd *cobra.Command, args []string) error {
	var data []*RadOutput
	file, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatal(err)
	}

	err = json.Unmarshal(file, &data)
	if err != nil {
		log.Fatal(err)
	}

	wg := sync.WaitGroup{}
	for _, r := range data {
		go func() {
			send(r)
			wg.Done()
		}()
		wg.Add(1)
	}
	wg.Wait()

	return nil
}

// Load json
func Load() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "load",
		Short: "load rad json file",
		RunE:  load,
	}
	cmd.Flags().StringVarP(&filePath, "file", "f", "test.json", "json file")
	cmd.Flags().StringVarP(&url, "server-url", "s", "http://127.0.0.1:8000/", "neat server url")

	return cmd
}

func main() {
	cmd := &cobra.Command{
		Use:   name,
		Short: name + ": " + version,
	}

	cmd.AddCommand(&cobra.Command{
		Use:   "version",
		Short: "show version",
		Run: func(_ *cobra.Command, _ []string) {
			i, _ := strconv.Atoi(buildstamp)
			t := time.Unix(int64(i), 0).Format("2006-01-02 15:04:05")
			fmt.Printf("Version: %s\nGithash: %s\nBuild: %s\n", version, githash, t)
		},
	})
	cmd.AddCommand(Load())
	if err := cmd.Execute(); err != nil {
		os.Exit(1)
	}
}
