from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader

# Настройка Jinja2
template_dir = 'templates'
env = Environment(loader=FileSystemLoader(template_dir))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path_parts = self.path.split('?', 1)
        path = path_parts[0]

        if path == '/':
            self.render_template('index.html', {'title': 'Главная - Прокат велосипедов'})
        elif path == '/catalog/':
            self.render_template('catalog.html', {'title': 'Каталог - Прокат велосипедов'})
        elif path == '/contact/':
            self.render_template('contact.html', {'title': 'Контакты - Прокат велосипедов'})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/contact/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            form_data = {}
            for pair in post_data.split('&'):
                key, value = pair.split('=', 1)
                form_data[key] = value

            name = form_data.get('name', '')
            email = form_data.get('email', '')

            self.render_template('contact.html',
                                 {'title': 'Контакты - Прокат велосипедов',
                                  'message': f'Спасибо, {name}! Мы свяжемся с Вами по email: {email}'})
        else:
            self.send_error(405)

    def render_template(self, template_name, data):
        template = env.get_template(template_name)
        html = template.render(**data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
