from flask import Flask, request, render_template
import os
import subprocess

app = Flask(__name__)

def write_to_history(shell_data):
    f = open("history.txt", "a")
    f.write(shell_data + "\n")

# Currently no error handling, so non-commands will fail non-gracefully.
def execute_command(command):
    f = open("shell.txt", "a")
    f.write(command + '\n')
    subprocess.check_call('{}'.format(command), shell=True, stdout=f)
    write_to_history(command)
    f.close()

@app.route('/', methods=['GET', 'POST'])
def lsof_output():
    if request.method == 'GET':
        op = open("shell.txt", "r").read()
        return render_template('index.html', output=op)
    if request.method == 'POST':
        port = request.form.to_dict()
        port = port['port']
        execute_command(port)
        op = open("shell.txt", "r").read()
        return render_template('index.html', output=op)