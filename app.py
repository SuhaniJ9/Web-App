from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import json
import mysql.connector

def establish_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="boot",
        database="sl_database"
    )

class RequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow cross-origin requests
        super().end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            with open('index.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse JSON data from frontend
        data = json.loads(post_data.decode('utf-8'))

        # Insert data into the database
        try:
            conn = establish_connection()
            cursor = conn.cursor()

            query = "INSERT INTO sl1 (username,password) VALUES (%s,  %s)"
            values = (data['username'], data['password'])
            cursor.execute(query, values)
            conn.commit()

            print("Data inserted successfully!")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Data inserted successfully!", "utf-8"))
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(bytes(f"Error: {e}", "utf-8"))

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server running at localhost:8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
