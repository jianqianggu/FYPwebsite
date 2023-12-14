from flask import Flask, request, jsonify, send_file, render_template
import os
import subprocess

app = Flask(__name__)

# Directory to store uploaded files and compiled binaries
UPLOAD_FOLDER = '/usr/src/app/src'
COMPILE_OUTPUT_FOLDER = '/usr/src/app/output'
CONSTRAINTS_PATH = '/usr/src/app/cons/constraints.xdc'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPILE_OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPILE_OUTPUT_FOLDER'] = COMPILE_OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'verilog_files' not in request.files:
        return jsonify({'message': 'No files part in the request'}), 400

    verilog_files = request.files.getlist('verilog_files')

    if not all(file.filename.endswith('.v') for file in verilog_files):
        return jsonify({'message': 'Invalid file type'}), 400

    saved_files = []
    for file in verilog_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        saved_files.append(file_path)

    compile_status, output, binary_file_path = compile_verilog(saved_files, constraints_file=None)

    if compile_status == 'Success':
        return send_file(binary_file_path, as_attachment=True)
    else:
        return jsonify({'message': 'Compilation failed', 'output': output})

def compile_verilog(verilog_files):
    # Replace with actual logic to compile files with Vivado
    # This is just a placeholder
    try:
        # Example command, modify according to your Vivado script and how you pass file paths
        command = f"vivado -mode batch -source your_vivado_script.tcl"
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Locate the compiled binary file
        # Replace this with the actual logic to locate the binary file
        binary_file_path = os.path.join(app.config['COMPILE_OUTPUT_FOLDER'], 'compiled_output.bit')

        return 'Success', result.stdout + '\n' + result.stderr, binary_file_path
    except subprocess.CalledProcessError as e:
        command = f"exit"
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return 'Error', str(e), None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
