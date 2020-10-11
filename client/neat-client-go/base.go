package client

import (
	"bytes"
	"encoding/json"
	"io"
	"io/ioutil"
)

type RequestDate struct {
	Auth       bool
	Method     string
	URI        string
	StatusCode int
}

type Request interface {
	ToPostData() (io.Reader, error)
	GetRequestData() *RequestDate
}

type BaseRequest struct {
	RequestDate *RequestDate
}

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
