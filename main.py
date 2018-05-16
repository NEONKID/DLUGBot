import json, os

from flask import Flask, request, jsonify
from messages import busmessage, mainmessage

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

keyboard = json.load(open('data/keyboard.json'))
busList = json.load(open('data/keyboard_Bus.json'))


@app.route('/message', methods=['POST'])
def postMessage():
    _req = request.get_json()
    try:
        for value in busList['buttons']:
            if _req['content'] == value:
                return jsonify(busmessage.getBusInfo(_req['content']))

        return jsonify(mainmessage.getResMessage(_req['content']))

    except KeyError:
        _msg = {
            "message": {
                "text": "Sorry, This comment no response message...."
            },

            "keyboard": keyboard
        }
        return jsonify(_msg)


@app.route('/keyboard', methods=['GET'])
def getKeyboard():
    return jsonify(keyboard)


@app.route('/')
def main():
    return 'hello D.L.U.G Chat Bot Server'


@app.errorhandler(404)
def page_not_found(err):
    _res = {
        'message': 'Page not found: ' + request.path,
        'success': 'false'
    }
    app.logger.error('Page not found: %s', (request.path))
    return jsonify(_res), 404


@app.errorhandler(405)
def method_not_allow(err):
    _res = {
        'message': 'Method not allowed: ' + request.path,
        'success': 'false'
    }
    app.logger.error('Method not allowed: %s', (request.path))
    return jsonify(_res), 405


@app.errorhandler(500)
def internal_server_error(err):
    _res = {
        'message': 'Server Error: ' + str(err),
        'success': 'false'
    }
    app.logger.error('Server Error: %s', (err))
    return jsonify(_res), 500


@app.errorhandler(Exception)
def unhandled_exception(err):
    _res = {
        'message': 'Unhandled Exception: ' + str(err),
        'success': 'false'
    }
    app.logger.error('Unhandled Exception: %s', (err))
    return jsonify(_res), 500


if __name__ == '__main__':
    app.run()
