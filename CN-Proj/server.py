import sys
import http.server
import socketserver

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Needs one argument: server port")
        raise SystemExit
    
    PORT = int(sys.argv[1])

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.allow_reuse_address=True
        print("Server started at localhost:" + str(PORT))
        httpd.serve_forever()