from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

hashmap = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/operate', methods=['POST'])
def operate():
    data = request.get_json()
    operation = data.get('operation')
    key = data.get('key')
    value = data.get('value')

    response = {"message": "", "hashmap": hashmap}

    if operation == 'insert':
        if key not in hashmap:
            hashmap[key] = []
        hashmap[key].append(value)
        response["message"] = f'Inserted "{value}" under key "{key}".'

    elif operation == 'search':
        if key in hashmap:
            response["message"] = f'Values for "{key}": {hashmap[key]}'
        else:
            response["message"] = f'Key "{key}" not found.'

    elif operation == 'delete':
        if key in hashmap:
            del hashmap[key]
            response["message"] = f'Deleted key "{key}".'
        else:
            response["message"] = f'Key "{key}" not found.'

    response["hashmap"] = hashmap
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
