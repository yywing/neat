from copy import deepcopy
from requests import Request, Session
from .model import HTTPSchema
from .model.raw import CreateRaw, CreateRawRequest, RawRespose
from .model.token import Token, VerifyToken, TokenRespose, GetTokenRequest, VerifyTokenRequest


DEFAULT_HEADERS = {"Content-Type": "application/json"}


class NeatClient():
    def __init__(self, base_url, username, password, session: Session = Session()):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = session

    def _send(self, auth, request: Request, timeout=10):
        if auth:
            token = self.auth()
            request.headers["Authorization"] = "JWT " + token
        prepped = self.session.prepare_request(request)
        resp = self.session.send(prepped, timeout=timeout)
        return resp

    def auth(self):
        if hasattr(self, "token"):
            try:
                data = VerifyTokenRequest.request_class(token=self.token)
                resp_data = self.verify_token(data)
                return self.token
            except Exception:
                pass
        data = Token.request_class(
            username=self.username, password=self.password)
        resp_data = self.get_token(data)
        self.token = resp_data.token
        return self.token

    def create_raw(self, data: CreateRawRequest, headers=deepcopy(DEFAULT_HEADERS)) -> RawRespose:
        m = CreateRaw(data)
        request = m.to_request(self.base_url, headers=headers)
        resp = self._send(m.auth, request)
        return m.from_response(resp)

    def get_token(self, data: GetTokenRequest, headers=deepcopy(DEFAULT_HEADERS)) -> TokenRespose:
        m = Token(data)
        request = m.to_request(self.base_url, headers=headers)
        resp = self._send(m.auth, request)
        return m.from_response(resp)

    def verify_token(self, data: VerifyTokenRequest, headers=deepcopy(DEFAULT_HEADERS)) -> TokenRespose:
        m = VerifyToken(data)
        request = m.to_request(self.base_url, headers=headers)
        resp = self._send(m.auth, request)
        return m.from_response(resp)


def main():
    client = NeatClient("http://127.0.0.1:8000/", "test", "test")
    data = CreateRaw.request_class(
        raw_request="R0VUIC9jb2RlZXhlYy9leGFtcGxlMy5waHA/bmV3PWhhY2tlciZwYXR0ZXJuPS9sYW1lci8mYmFzZT1IZWxsbyUyMGxhbWVyIEhUVFAvMS4xDQpIb3N0OiBwZW50ZXN0ZXItd2ViLnZ1bG5ldA0KQWNjZXB0OiAqLyoNClJlZmVyZXI6IGh0dHA6Ly9wZW50ZXN0ZXItd2ViLnZ1bG5ldC8NClVzZXItQWdlbnQ6IE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdPVzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzEuMC4zNTc4Ljk4IFNhZmFyaS81MzcuMzYNCg0K",
        raw_response="SFRUUC8xLjEgMjAwIE9LDQpDb250ZW50LUxlbmd0aDogMTQ1OQ0KQ29udGVudC1UeXBlOiB0ZXh0L2h0bWwNCkRhdGU6IEZyaSwgMzEgSnVsIDIwMjAgMDc6MDI6NDMgR01UDQpTZXJ2ZXI6IEFwYWNoZS8yLjIuMTYgKERlYmlhbikNClZhcnk6IEFjY2VwdC1FbmNvZGluZw0KWC1Qb3dlcmVkLUJ5OiBQSFAvNS4zLjMtNytzcXVlZXplMTUNClgtWHNzLVByb3RlY3Rpb246IDANCg0KPCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KICA8aGVhZD4KICAgIDxtZXRhIGNoYXJzZXQ9InV0Zi04Ij4KICAgIDx0aXRsZT5QZW50ZXN0ZXJMYWIgJnJhcXVvOyBXZWIgZm9yIFBlbnRlc3RlcjwvdGl0bGU+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEuMCI+CiAgICA8bWV0YSBuYW1lPSJkZXNjcmlwdGlvbiIgY29udGVudD0iV2ViIEZvciBQZW50ZXN0ZXIiPgogICAgPG1ldGEgbmFtZT0iYXV0aG9yIiBjb250ZW50PSJMb3VpcyBOeWZmZW5lZ2dlciAobG91aXNAcGVudGVzdGVybGFiLmNvbSkiPgoKICAgIDwhLS0gTGUgc3R5bGVzIC0tPgogICAgPGxpbmsgaHJlZj0iL2Nzcy9ib290c3RyYXAuY3NzIiByZWw9InN0eWxlc2hlZXQiPgoKICAgIDxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+CiAgICAgIGJvZHkgewogICAgICAgIHBhZGRpbmctdG9wOiA2MHB4OwogICAgICAgIHBhZGRpbmctYm90dG9tOiA0MHB4OwogICAgICB9CiAgICA8L3N0eWxlPgogICAgPGxpbmsgaHJlZj0iL2Nzcy9ib290c3RyYXAtcmVzcG9uc2l2ZS5jc3MiIHJlbD0ic3R5bGVzaGVldCI+CgogIDwvaGVhZD4KCiAgPGJvZHk+CgogICAgPGRpdiBjbGFzcz0ibmF2YmFyIG5hdmJhci1pbnZlcnNlIG5hdmJhci1maXhlZC10b3AiPgogICAgICA8ZGl2IGNsYXNzPSJuYXZiYXItaW5uZXIiPgogICAgICAgIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgICAgICA8YSBjbGFzcz0iYnRuIGJ0bi1uYXZiYXIiIGRhdGEtdG9nZ2xlPSJjb2xsYXBzZSIgZGF0YS10YXJnZXQ9Ii5uYXYtY29sbGFwc2UiPgogICAgICAgICAgICA8c3BhbiBjbGFzcz0iaWNvbi1iYXIiPjwvc3Bhbj4KICAgICAgICAgICAgPHNwYW4gY2xhc3M9Imljb24tYmFyIj48L3NwYW4+CiAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJpY29uLWJhciI+PC9zcGFuPgogICAgICAgICAgPC9hPgogICAgICAgICAgPGEgY2xhc3M9ImJyYW5kIiBocmVmPSJodHRwczovL3BlbnRlc3RlcmxhYi5jb20vIj5QZW50ZXN0ZXJMYWIuY29tPC9hPgogICAgICAgICAgPGRpdiBjbGFzcz0ibmF2LWNvbGxhcHNlIGNvbGxhcHNlIj4KICAgICAgICAgICAgPHVsIGNsYXNzPSJuYXYiPgogICAgICAgICAgICAgIDxsaSBjbGFzcz0iYWN0aXZlIj48YSBocmVmPSIvIj5Ib21lPC9hPjwvbGk+CiAgICAgICAgICAgIDwvdWw+CiAgICAgICAgICA8L2Rpdj48IS0tLy5uYXYtY29sbGFwc2UgLS0+CiAgICAgICAgPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0iY29udGFpbmVyIj4KCgoKSGVsbG8gaGFja2VyCgogICAgICA8Zm9vdGVyPgogICAgICAgIDxwPiZjb3B5OyBQZW50ZXN0ZXJMYWIgMjAxMzwvcD4KICAgICAgPC9mb290ZXI+CgogICAgPC9kaXY+IDwhLS0gL2NvbnRhaW5lciAtLT4KCgogIDwvYm9keT4KPC9odG1sPgoKCg==",
        scheme=HTTPSchema.HTTP.value,
        host="1.1.1.1",
        port=80,
    )
    resp_data = client.create_raw(data)
    print(resp_data)


if __name__ == "__main__":
    main()
