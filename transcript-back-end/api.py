from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

# Define your API endpoints here
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'key': 'value'}
    return jsonify(data)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)  # Debug mode allows you to see changes without restarting the server