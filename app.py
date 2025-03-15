from flask import Flask, request, jsonify, render_template, Response
import os
import subprocess

app = Flask(__name__)

SQUID_CONFIG_FILE = '/etc/squid/squid.conf'

# Ensure the squid.conf file exists
if not os.path.exists(SQUID_CONFIG_FILE):
    with open(SQUID_CONFIG_FILE, 'w') as f:
        f.write("# Squid Configuration\n\n")

# Helper function to read squid.conf and split into blocks
def read_config_blocks():
    blocks = {
        "basic": [],
        "acls": [],
        "allow_access": [],
        "deny_access": [],
        "cache_settings": [],
        "logging": [],
        "dns_settings": []
    }
    current_block = None

    with open(SQUID_CONFIG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("# Basic Squid Configuration"):
                current_block = "basic"
            elif line.startswith("# Access Control Lists (ACLs)"):
                current_block = "acls"
            elif line.startswith("# Allow access from localnet and localhost"):
                current_block = "allow_access"
            elif line.startswith("# Deny all other access"):
                current_block = "deny_access"
            elif line.startswith("# Cache Settings"):
                current_block = "cache_settings"
            elif line.startswith("# Logging"):
                current_block = "logging"
            elif line.startswith("# DNS Settings"):
                current_block = "dns_settings"
            elif line.startswith("#") or not line:
                continue  # Skip comments and empty lines
            elif current_block:
                blocks[current_block].append(line)

    return blocks

# Helper function to write blocks back to squid.conf
def write_config_blocks(blocks):
    with open(SQUID_CONFIG_FILE, 'w') as f:
        f.write("# Squid Configuration\n\n")
        f.write("# Basic Squid Configuration\n")
        f.writelines([line + "\n" for line in blocks["basic"]])
        f.write("\n# Access Control Lists (ACLs)\n")
        f.writelines([line + "\n" for line in blocks["acls"]])
        f.write("\n# Allow access from localnet and localhost\n")
        f.writelines([line + "\n" for line in blocks["allow_access"]])
        f.write("\n# Deny all other access\n")
        f.writelines([line + "\n" for line in blocks["deny_access"]])
        f.write("\n# Cache Settings\n")
        f.writelines([line + "\n" for line in blocks["cache_settings"]])
        f.write("\n# Logging\n")
        f.writelines([line + "\n" for line in blocks["logging"]])
        f.write("\n# DNS Settings\n")
        f.writelines([line + "\n" for line in blocks["dns_settings"]])

# Get a specific block
@app.route('/config/<block>', methods=['GET'])
def get_block(block):
    blocks = read_config_blocks()
    if block not in blocks:
        return jsonify({"error": "Invalid block name"}), 400
    return jsonify({block: blocks[block]})

# Update a specific block
@app.route('/config/<block>', methods=['POST'])
def update_block(block):
    data = request.json
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input. Expected a list of lines."}), 400

    blocks = read_config_blocks()
    if block not in blocks:
        return jsonify({"error": "Invalid block name"}), 400

    blocks[block] = data
    write_config_blocks(blocks)
    return jsonify({"message": f"Block '{block}' updated successfully."})

# Get the entire configuration
@app.route('/config', methods=['GET'])
def get_config():
    blocks = read_config_blocks()  # Function to read and parse squid.conf
    return jsonify(blocks)

# render log viewer
@app.route('/logs')
def get_logs():
    def generate():
        with open('/var/log/squid/access.log', 'r') as f:
            f.seek(0, 2)  # Move to the end of the file
            while True:
                line = f.readline()
                if not line:
                    break
                yield f"{line}<br>"
    return Response(generate(), mimetype='text/html')

# Reload Squid configuration
@app.route('/reload', methods=['POST'])
def reload_squid():
    try:
        # Execute the Squid reload command
        result = subprocess.run(['sudo', 'squid', '-k', 'reconfigure'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Squid configuration reloaded successfully."})
        else:
            return jsonify({"error": f"Failed to reload Squid configuration: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Check Squid configuration syntax
@app.route('/check-syntax', methods=['GET'])
def check_syntax():
    try:
        # Run the squid -k parse command to check syntax
        result = subprocess.run(['sudo', 'squid', '-k', 'parse'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Syntax is valid.", "output": result.stdout})
        else:
            return jsonify({"error": "Syntax check failed.", "output": result.stderr}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Serve the main HTML template
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)