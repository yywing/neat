package client

import (
	"context"
	"fmt"
	"net/http"
)

var (
	DefaultHeader = map[string]string{"Content-Type": "application/json"}
)

const (
	API_PREFIX = "/api/"
)

type NeatClient struct {
	BaseURL  string
	Client   *http.Client
	Username string
	Password string
	token    string
}

func NewNeatClient(baseUrl, username, password string, client *http.Client) *NeatClient {
	return &NeatClient{
		BaseURL:  baseUrl,
		Client:   client,
		Username: username,
		Password: password,
	}
}

func (c *NeatClient) Auth(ctx context.Context) (string, error) {
	if c.token != "" {
		req := &VerifyTokenRequest{
			Token: c.token,
		}
		_, err := c.VerifyToken(ctx, CopyMap(DefaultHeader), req)
		if err == nil {
			return c.token, nil
		}
	}

	req := &GetTokenRequest{
		Username: c.Username,
		Password: c.Password,
	}
	resp, err := c.GetToken(ctx, CopyMap(DefaultHeader), req)
	if err != nil {
		return "", err
	}
	c.token = resp.Token
	return resp.Token, nil
}

func (c *NeatClient) send(ctx context.Context, header map[string]string, request Request, response Response) error {
	requestData := request.GetRequestData()
	url := JoinURL(c.BaseURL, requestData.URI)
	//fmt.Printf("%s %s \n", method, url)
	reader, err := request.ToPostData()
	if err != nil {
		return err
	}
	req, err := http.NewRequestWithContext(ctx, requestData.Method, url, reader)
	for k, v := range header {
		req.Header.Set(k, v)
	}
	if requestData.Auth {
		token, err := c.Auth(ctx)
		if err != nil {
			return err
		}
		req.Header.Set("Authorization", "JWT "+token)
	}
	if err != nil {
		return err
	}
	resp, err := c.Client.Do(req)
	if err != nil {
		return err
	}
	if resp.StatusCode != requestData.StatusCode {
		return fmt.Errorf("want status code %v, but got %v. response content: %s", requestData.StatusCode, resp.StatusCode, resp.Body)
	}
	err = response.ToStruct(resp.Body)
	if err != nil {
		return err
	}
	return nil
}
