from flask import Flask, render_template, request
import copy

app = Flask(__name__)

# Define the queue
queue = []

# Define the processed users list
processed_users = []

# Define the maximum number of tickets
MAX_TICKETS = 10

# Define the queue operations
def is_empty(queue):
    return len(queue) == 0

def is_full(queue):
    return len(queue) == MAX_TICKETS

def length(queue):
    return len(queue)

def insert(queue, item):
    if not is_full(queue):
        queue.append(item)
        return True
    return False

def remove(queue):
    if not is_empty(queue):
        return queue.pop(0)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None

    if request.method == 'POST':
        name = request.form['name']
        payment = request.form.get('payment')

        if name.strip() and payment == 'paid':
            if not is_full(queue):
                if ' ' in name:
                    first_name, last_name = name.split()
                    ticket = {'name': f'{first_name} {last_name}'}
                    insert(queue, ticket)
                else:
                    error = 'Please enter both your first and last name.'
            else:
                error = 'Sorry, all tickets have been sold.'
        else:
            error = 'Please enter a valid name and confirm payment.'

    return render_template('index.html', queue=copy.deepcopy(queue), processed_users=processed_users, processed_count=len(processed_users), error=error)

@app.route('/process', methods=['POST'])
def process_ticket():
    if not is_empty(queue):
        ticket = remove(queue)
        processed_users.append(ticket['name'])
    return render_template('index.html', queue=copy.deepcopy(queue), processed_users=processed_users, processed_count=len(processed_users), error=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
