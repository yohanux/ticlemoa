from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import ssl

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # CORS 헤더 설정
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/xml')
        self.end_headers()
        
        # URL 파라미터 파싱
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if 'url' not in params:
            self.wfile.write(b'URL parameter is required')
            return
            
        target_url = params['url'][0]
        
        try:
            # SSL 인증서 검증 비활성화 (개발 환경용)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            # RSS 피드 요청
            req = urllib.request.Request(
                target_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; RSS Reader Bot/1.0)'
                }
            )
            
            with urllib.request.urlopen(req, context=ctx) as response:
                self.wfile.write(response.read())
                
        except Exception as e:
            self.wfile.write(str(e).encode())

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ProxyHandler)
    print('Starting proxy server on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 