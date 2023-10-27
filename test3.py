from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


webhook_url = 'https://hooks.slack.com/services/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'


@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        message = data.get('message', 'Hello from the Flask app using Slack webhook!')

        payload = {
            'channel': '#bot-testing', 
            'text': message
        }

        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  
        return jsonify({"status": "success", "message": "Message sent successfully!"}), 200
    except requests.exceptions.HTTPError as errh:
        return jsonify({"status": "error", "message": f"HTTP Error: {errh}"}), 500
    except requests.exceptions.ConnectionError as errc:
        return jsonify({"status": "error", "message": f"Error Connecting: {errc}"}), 500
    except requests.exceptions.Timeout as errt:
        return jsonify({"status": "error", "message": f"Timeout Error: {errt}"}), 500
    except requests.exceptions.RequestException as err:
        return jsonify({"status": "error", "message": f"OOps: Something Else {err}"}), 500

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
