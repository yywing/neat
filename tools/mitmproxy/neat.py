"""HTTP-specific events."""
import base64
import mitmproxy.http
from mitmproxy import ctx
from mitmproxy.net.http.http1 import assemble
from neat_client_python import client


class Neat:
    def load(self, loader):
        loader.add_option(
            name="neat_url",
            typespec=str,
            default="",
            help="neat server url",
        )
        loader.add_option(
            name="neat_username",
            typespec=str,
            default="",
            help="neat server username",
        )
        loader.add_option(
            name="neat_password",
            typespec=str,
            default="",
            help="neat server password",
        )

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if not hasattr(self, "client"):
            self.client = client.NeatClient(
                ctx.options.neat_url, ctx.options.neat_username, ctx.options.neat_password
            )
        data = client.CreateRaw.request_class(
            raw_request=base64.b64encode(
                assemble.assemble_request(flow.request)
            ).decode('ascii'),
            raw_response=base64.b64encode(
                assemble.assemble_response(flow.response)
            ).decode('ascii'),
            scheme=flow.request.scheme,
            host=flow.request.host,
            port=flow.request.port,
        )
        self.client.create_raw(data)


addons = [
    Neat()
]
