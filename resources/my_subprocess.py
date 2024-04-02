import subprocess
import time
import os

# Start the Ollama service in the background
ollama_serve_command = "Ollama serve &"
subprocess.run(ollama_serve_command, shell=True)

# Add a delay to allow the service to start (adjust as needed)
time.sleep(5)

def open_terminal_with_commands(*cmds):
    for cmd in cmds:
        subprocess.run(['osascript', '-e', f'tell app "Terminal" to do 
script "{cmd}"'])
    # Close the terminal window after commands are done
    os.system('osascript -e \'tell application "Terminal" to close first 
window\'')

# Run command in a new Terminal tab:
commands_in_new_tab = [
    'Ollama run llama2',
]
open_terminal_with_commands(*commands_in_new_tab)

# Wait for the Ollama service to be ready and listen on port 11434
while True:
    try:
        # Run the command to ask a question to llama2
        ollama_run_command = 'curl http://localhost:11434/api/chat -d 
\'{"model": "llama2", "messages": [{"role": "user", "content": "what is 
the second law of thermodynamics?"}]}\''
        result = subprocess.run(ollama_run_command, shell=True, 
stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print the output
        print("Output:", result.stdout)
        
        # Check if there were any errors in our command execution
        if result.stderr:
            print("Errors:", result.stderr)
            
        # The return code will be 0 if it ran successfully, otherwise it's
non-zero.
        if result.returncode != 0:
            raise Exception(f"Subprocess returned with error code 
{result.returncode}")
        
        break
     except Exception as e:
         print("Exception encountered:", str(e))
         continue

