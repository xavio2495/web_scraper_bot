import scraper
from flask import Flask, render_template, request, send_file, jsonify, flash
import os
import tempfile
from io import StringIO
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_data():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    df= scraper.main(url)
    # Generate filename like in your original code
    try:
        filename = url.split('=')[1].split('&')[0] + '.csv'
    except:
        filename = 'shareholding_data.csv'
    # Save to temporary file
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, filename)
    df.to_csv(filepath, index=False)
    return jsonify({
        'success': True,
        'filename': filename,
        'rows': len(df),
        'message': 'Data scraped successfully'
        })

@app.route('/download/<filename>')
def download_file(filename):
    try:
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)