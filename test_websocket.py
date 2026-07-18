import tornado.testing
import tornado.web
import tornado.websocket
import urllib.parse
from tornado.httpclient import HTTPRequest
from argos import WebSocketServer, getConfig

class TestWebSocketOrigin(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
            (r'/ws', WebSocketServer),
        ])

    @tornado.testing.gen_test
    async def test_websocket_origin_allowed(self):
        ws_url = "ws://127.0.0.1:%d/ws" % self.get_http_port()
        # Tornado checks if the origin domain matches the host header.
        request = HTTPRequest(
            url=ws_url,
            headers={"Origin": "http://127.0.0.1:%d" % self.get_http_port(),
                     "Host": "127.0.0.1:%d" % self.get_http_port()}
        )
        try:
            ws = await tornado.websocket.websocket_connect(request)
            self.assertTrue(True)
            ws.close()
        except Exception as e:
            self.fail(f"Connection failed: {e}")

    @tornado.testing.gen_test
    async def test_websocket_origin_rejected(self):
        ws_url = "ws://127.0.0.1:%d/ws" % self.get_http_port()
        request = HTTPRequest(
            url=ws_url,
            headers={"Origin": "http://evil.com",
                     "Host": "127.0.0.1:%d" % self.get_http_port()}
        )
        try:
            ws = await tornado.websocket.websocket_connect(request)
            self.fail("Connection should have been rejected")
        except Exception as e:
            self.assertEqual(e.code, 403)

if __name__ == '__main__':
    tornado.testing.main()
