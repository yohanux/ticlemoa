from flask import Flask, request, Response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return {'error': 'URL parameter is required'}, 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; RSSFeedReader/1.0;)'
        }
        response = requests.get(url, headers=headers)
        return Response(
            response.content,
            content_type='application/xml',
            status=response.status_code
        )
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(port=3000) 