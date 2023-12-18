'''
python3 shell_exec.py jsub -N job cats.sh
python3 shell_exec.py /usr/bin/toolforge jobs run mvn11 --image python3.9 --command ""
'''
import subprocess
import sys

def execute_command(command):
    if command.endswith('.sh'):
        # read the contents of the file
        with open(command, 'r') as f:
            command = f.read()
    # execute the command
    print(command)
    try:
        result = subprocess.call(command, shell=True)
        print(result)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # print("Usage: python3 shell_exec.py <command>")
        sys.exit(1)

    command_to_execute = " ".join(sys.argv[1:])
    execute_command(command_to_execute)
