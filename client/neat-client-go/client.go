package client

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
)

var (
	DefaultHeader = map[string]string{"Content-Type": "application/json"}
)

const (
	API_PREFIX = "/api/"
)

type Request interface {
	ToPostData() (io.Reader, error)
}

type BaseRequest struct{}

func (*BaseRequest) toPostData(r interface{}) (io.Reader, error) {
	bytesData, err := json.Marshal(r)

	if err != nil {
		return nil, err
	}
	return bytes.NewReader(bytesData), nil
}

type Response interface {
	ToStruct(io.Reader) error
}

type BaseResponse struct{}

func (*BaseResponse) toStruct(r interface{}, reader io.Reader) error {
	body, err := ioutil.ReadAll(reader)
	if err != nil {
		return err
	}
	err = json.Unmarshal(body, r)
	return err
}

type NeatClient struct {
	BaseURL string
	Client  *http.Client
}

func NewNeatClient(baseUrl string, client *http.Client) *NeatClient {
	return &NeatClient{
		BaseURL: baseUrl,
		Client:  client,
	}
}

func (c *NeatClient) send(ctx context.Context, method, uri string, exceptStatusCode int, headers map[string]string, request Request, response Response) error {
	url := JoinURL(c.BaseURL, uri)
	//fmt.Printf("%s %s \n", method, url)
	reader, err := request.ToPostData()
	if err != nil {
		return err
	}
	req, err := http.NewRequestWithContext(ctx, method, url, reader)
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	if err != nil {
		return err
	}
	resp, err := c.Client.Do(req)
	if err != nil {
		return err
	}
	if resp.StatusCode != exceptStatusCode {
		return fmt.Errorf("resp status code error: %v", resp.StatusCode)
	}
	err = response.ToStruct(resp.Body)
	if err != nil {
		return err
	}
	return nil
}
