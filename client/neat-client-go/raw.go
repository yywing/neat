package client

import (
	"context"
	"io"
	"net/http"
)

type Scheme string

const (
	HTTP  = Scheme("http")
	HTTPS = Scheme("https")
)

type CreateRawRequest struct {
	BaseRequest
	RawRequest  string `json:"raw_request"`
	RawResponse string `json:"raw_response,omitempty"`
	Scheme      Scheme `json:"scheme"`
	Host        string `json:"host"`
	Port        uint16 `json:"port"`
}

func (r *CreateRawRequest) GetRequestData() *RequestDate {
	if r.RequestDate == nil {
		r.RequestDate = &RequestDate{
			Auth:       true,
			Method:     http.MethodPost,
			URI:        JoinURL(API_PREFIX, "/raw/"),
			StatusCode: http.StatusCreated,
		}
	}
	return r.RequestDate
}

func (r *CreateRawRequest) ToPostData() (io.Reader, error) {
	return r.toPostData(r)
}

type RawResponse struct {
	BaseResponse
	Id          int64  `json:"id"`
	RawRequest  string `json:"raw_request"`
	RawResponse string `json:"raw_response,omitempty"`
	Scheme      Scheme `json:"scheme"`
	Host        string `json:"host"`
	Port        uint16 `json:"port"`
	CreatedTime string `json:"created_time"`
	URL         int64  `json:"url"`
}

func (r *RawResponse) ToStruct(reader io.Reader) error {
	return r.toStruct(r, reader)
}

func (c *NeatClient) CreateRaw(ctx context.Context, header map[string]string, request *CreateRawRequest) (*RawResponse, error) {
	response := &RawResponse{}
	err := c.send(ctx, header, request, response)
	return response, err
}
