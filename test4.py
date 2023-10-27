from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)


@app.route('/slack', methods=['POST'])
def slack_webhook():
    data = request.get_json()

    message_text = data.get('text')

    processed_message = f'You sent: {message_text}'

    response_message = {
        'text': processed_message
    }
    webhook_url = 'https://hooks.slack.com/services/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/slack'

    requests.post(webhook_url, json=response_message)

    # Return a response to the original Slack request
    return jsonify({'message': 'Message received and processed successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
