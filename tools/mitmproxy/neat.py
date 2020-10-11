"""HTTP-specific events."""
import base64
import mitmproxy.http
from mitmproxy import ctx
from mitmproxy.net.http.http1 import assemble
from neat_client_python import client, model


class Neat:
    def load(self, loader):
        loader.add_option(
            name="neat_url",
            typespec=str,
            default=None,
            help="neat server url",
        )

    def configure(self, updates):
        self.client = client.NeatClient(ctx.options.neat_url)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        data = model.CreateRaw.request_class(
            raw_request=base64.b64encode(
                assemble.assemble_request(flow.request)
            ),
            raw_response=base64.b64encode(
                assemble.assemble_response(flow.response)
            ),
            scheme=flow.request.scheme,
            host=flow.request.host,
            port=flow.request.port,
        )
        resp_data = self.client.create_raw(data)
        print(resp_data)


addons = [
    Neat()
]
