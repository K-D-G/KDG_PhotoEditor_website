from flask import Flask, render_template, send_file, request, send_from_directory

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("/static/html/index.html")

@app.route('/downloads')
def downloads():
    platform=request.args.get('platform')
    version=request.args.get('version')
    if platform and version:
        file_extension=''
        if platform=='windows':
            file_extension='.exe'
        elif platform=='macos':
            file_extension='.dmg'
        return send_file('/static/downloads/version_{}/KDG_PhotoEditor{}'.format(version, file_extension), attachment_filename='KDG_PhotoEditor{}'.format(file_extension))
    return render_template("/static/html/downloads.html")

@app.route('/about')
def about():
    return render_template('/static/html/about.html')

@app.route('/static', methods=["GET"])
def static_serve():
    return send_from_directory('templates/static', request.args.get('path'))

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
