package main

import (
	"context"
	"fmt"
	"net/http"

	client "github.com/yywing/neat/client/neat-client-go"
)

func main() {
	c := &http.Client{}
	baseURL := `http://127.0.0.1:8000/`
	neatClient := client.NewNeatClient(baseURL, "test", "test", c)
	req := &client.CreateRawRequest{
		RawRequest:  "R0VUIC9jb2RlZXhlYy9leGFtcGxlMy5waHA/bmV3PWhhY2tlciZwYXR0ZXJuPS9sYW1lci8mYmFzZT1IZWxsbyUyMGxhbWVyIEhUVFAvMS4xDQpIb3N0OiBwZW50ZXN0ZXItd2ViLnZ1bG5ldA0KQWNjZXB0OiAqLyoNClJlZmVyZXI6IGh0dHA6Ly9wZW50ZXN0ZXItd2ViLnZ1bG5ldC8NClVzZXItQWdlbnQ6IE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdPVzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzEuMC4zNTc4Ljk4IFNhZmFyaS81MzcuMzYNCg0K",
		RawResponse: "SFRUUC8xLjEgMjAwIE9LDQpDb250ZW50LUxlbmd0aDogMTQ1OQ0KQ29udGVudC1UeXBlOiB0ZXh0L2h0bWwNCkRhdGU6IEZyaSwgMzEgSnVsIDIwMjAgMDc6MDI6NDMgR01UDQpTZXJ2ZXI6IEFwYWNoZS8yLjIuMTYgKERlYmlhbikNClZhcnk6IEFjY2VwdC1FbmNvZGluZw0KWC1Qb3dlcmVkLUJ5OiBQSFAvNS4zLjMtNytzcXVlZXplMTUNClgtWHNzLVByb3RlY3Rpb246IDANCg0KPCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KICA8aGVhZD4KICAgIDxtZXRhIGNoYXJzZXQ9InV0Zi04Ij4KICAgIDx0aXRsZT5QZW50ZXN0ZXJMYWIgJnJhcXVvOyBXZWIgZm9yIFBlbnRlc3RlcjwvdGl0bGU+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEuMCI+CiAgICA8bWV0YSBuYW1lPSJkZXNjcmlwdGlvbiIgY29udGVudD0iV2ViIEZvciBQZW50ZXN0ZXIiPgogICAgPG1ldGEgbmFtZT0iYXV0aG9yIiBjb250ZW50PSJMb3VpcyBOeWZmZW5lZ2dlciAobG91aXNAcGVudGVzdGVybGFiLmNvbSkiPgoKICAgIDwhLS0gTGUgc3R5bGVzIC0tPgogICAgPGxpbmsgaHJlZj0iL2Nzcy9ib290c3RyYXAuY3NzIiByZWw9InN0eWxlc2hlZXQiPgoKICAgIDxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+CiAgICAgIGJvZHkgewogICAgICAgIHBhZGRpbmctdG9wOiA2MHB4OwogICAgICAgIHBhZGRpbmctYm90dG9tOiA0MHB4OwogICAgICB9CiAgICA8L3N0eWxlPgogICAgPGxpbmsgaHJlZj0iL2Nzcy9ib290c3RyYXAtcmVzcG9uc2l2ZS5jc3MiIHJlbD0ic3R5bGVzaGVldCI+CgogIDwvaGVhZD4KCiAgPGJvZHk+CgogICAgPGRpdiBjbGFzcz0ibmF2YmFyIG5hdmJhci1pbnZlcnNlIG5hdmJhci1maXhlZC10b3AiPgogICAgICA8ZGl2IGNsYXNzPSJuYXZiYXItaW5uZXIiPgogICAgICAgIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgICAgICA8YSBjbGFzcz0iYnRuIGJ0bi1uYXZiYXIiIGRhdGEtdG9nZ2xlPSJjb2xsYXBzZSIgZGF0YS10YXJnZXQ9Ii5uYXYtY29sbGFwc2UiPgogICAgICAgICAgICA8c3BhbiBjbGFzcz0iaWNvbi1iYXIiPjwvc3Bhbj4KICAgICAgICAgICAgPHNwYW4gY2xhc3M9Imljb24tYmFyIj48L3NwYW4+CiAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJpY29uLWJhciI+PC9zcGFuPgogICAgICAgICAgPC9hPgogICAgICAgICAgPGEgY2xhc3M9ImJyYW5kIiBocmVmPSJodHRwczovL3BlbnRlc3RlcmxhYi5jb20vIj5QZW50ZXN0ZXJMYWIuY29tPC9hPgogICAgICAgICAgPGRpdiBjbGFzcz0ibmF2LWNvbGxhcHNlIGNvbGxhcHNlIj4KICAgICAgICAgICAgPHVsIGNsYXNzPSJuYXYiPgogICAgICAgICAgICAgIDxsaSBjbGFzcz0iYWN0aXZlIj48YSBocmVmPSIvIj5Ib21lPC9hPjwvbGk+CiAgICAgICAgICAgIDwvdWw+CiAgICAgICAgICA8L2Rpdj48IS0tLy5uYXYtY29sbGFwc2UgLS0+CiAgICAgICAgPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0iY29udGFpbmVyIj4KCgoKSGVsbG8gaGFja2VyCgogICAgICA8Zm9vdGVyPgogICAgICAgIDxwPiZjb3B5OyBQZW50ZXN0ZXJMYWIgMjAxMzwvcD4KICAgICAgPC9mb290ZXI+CgogICAgPC9kaXY+IDwhLS0gL2NvbnRhaW5lciAtLT4KCgogIDwvYm9keT4KPC9odG1sPgoKCg==",
		Scheme:      client.HTTP,
		Host:        "1.1.1.1",
		Port:        80,
	}
	ctx := context.Background()
	resp, err := neatClient.CreateRaw(ctx, client.CopyMap(client.DefaultHeader), req)
	if err != nil {
		fmt.Printf("request err: %v", err)
	} else {
		fmt.Printf("request success, response: %v", resp)
	}
}
