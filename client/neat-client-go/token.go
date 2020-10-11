package client

import (
	"context"
	"io"
	"net/http"
)

var (
	TOKEN_URI = JoinURL(API_PREFIX, "/token/")
)

type GetTokenRequest struct {
	BaseRequest
	Username string `json:"username"`
	Password string `json:"password"`
}

func (r *GetTokenRequest) ToPostData() (io.Reader, error) {
	return r.toPostData(r)
}

type TokenResponse struct {
	BaseResponse
	Token string `json:"token"`
}

func (r *GetTokenRequest) GetRequestData() *RequestDate {
	if r.RequestDate == nil {
		r.RequestDate = &RequestDate{
			Auth:       false,
			Method:     http.MethodPost,
			URI:        TOKEN_URI,
			StatusCode: http.StatusOK,
		}
	}
	return r.RequestDate
}

func (r *TokenResponse) ToStruct(reader io.Reader) error {
	return r.toStruct(r, reader)
}

func (c *NeatClient) GetToken(ctx context.Context, header map[string]string, request *GetTokenRequest) (*TokenResponse, error) {
	response := &TokenResponse{}
	err := c.send(ctx, header, request, response)
	return response, err
}

type VerifyTokenRequest struct {
	BaseRequest
	Token string `json:"token"`
}

func (r *VerifyTokenRequest) GetRequestData() *RequestDate {
	if r.RequestDate == nil {
		r.RequestDate = &RequestDate{
			Auth:       false,
			Method:     http.MethodPost,
			URI:        JoinURL(TOKEN_URI, "/verify"),
			StatusCode: http.StatusOK,
		}
	}
	return r.RequestDate
}

func (r *VerifyTokenRequest) ToPostData() (io.Reader, error) {
	return r.toPostData(r)
}

func (c *NeatClient) VerifyToken(ctx context.Context, header map[string]string, request *VerifyTokenRequest) (*TokenResponse, error) {
	response := &TokenResponse{}
	err := c.send(ctx, header, request, response)
	return response, err
}
