from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        arr_str = request.form['array']
        key = int(request.form['key'])
        arr = [int(x.strip()) for x in arr_str.split(',')]
    except ValueError:
        return render_template('index.html', error="Please enter valid integers.")

    steps = []  
    n = len(arr)
    last = arr[-1]
    arr[-1] = key  

    i = 0
    while arr[i] != key:
        steps.append(f"Iteration {i+1}: compared {key} with {arr[i]} — not found yet")
        i += 1

    arr[-1] = last  

    if i < n-1 or arr[-1] == key:
        result = f"Key {key} found at index {i}"
    else:
        result = f"Key {key} not found"

    steps.append(f"Iteration {i+1}: compared {key} with {arr[i]} — match found!")

    return render_template('result.html', array=arr, key=key, steps=steps, result=result)


@app.route('/algorithm')
def algorithm():  
    return render_template('algorithm.html')

if __name__ == '__main__':
    app.run(debug=True)