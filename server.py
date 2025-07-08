import subprocess
import os
import sys
import json

dir = os.path.dirname(os.path.abspath(__file__))
server_jar = os.path.join(dir, 'server.jar')
logs = {}
if os.path.exists('logs_py.txt'):
    with open('logs_py.txt', 'r') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = {}
else:
    with open('logs_py.txt', 'w')as f:
        json.dump({}, f)

java_command = ['java', '-Xmx3072M', '-Xms2072M', '-jar', 'server.jar', 'nogui']

def main():
    input('Por favor guarda tu archivo jar del servidor en la misma carpeta que este script, llamalo "server.jar" y presiona enter...')
    if not os.path.exists(server_jar):
        print('Error: No se ha encontrado el archivo server.jar, asegurate de que se llama "server.jar" y está en la misma carpeta que este script')
        sys.exit(1)
    os.chdir(dir)
    selected = int(input('''     Menú
1-Iniciar servidor
2-Añadir log
3-Borrar log
4-Iniciar playit
5-Salir
--------- '''))
    if selected == 1:
        try:
            os.system('echo eula = true > eula.txt')

            process = subprocess.Popen(java_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE, text = True)

            while True:
                log = process.stdout.readline()
                print(log)

                if not log and process.poll() is not None:
                    break

                for log_in_logs in logs:
                    if log_in_logs in log:
                        process.stdin.write(logs[log_in_logs] + '\n')
                        process.stdin.flush()
        
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)

    elif selected == 2:
        add = str(input('Que log queres añadir? '))
        if not add:
            print('Por favor, escribe algo')
            sys.exit(1)
        execute = str(input('Que comando quieres ejecutar? '))
        if not execute:
            print('Por favor, escribe algo')
            sys.exit(1)
        if not logs[add]:
            logs[add] = execute
            with open('logs_py.txt', 'w') as f:
                json.dump(logs, f, indent = 4)
            main()
        else:
            print('Ese ya esta creado!')
            sys.exit(1)
        

    elif selected == 3:
        if logs:
            print('Estos son los logs creados:')
            for log in logs:
                print(f'-{log} -> {logs[log]}')
            log_to_remove = str(input('--------- '))
            if not log_to_remove:
                print('Por favor, introduce un log')
                sys.exit(1)
            if not log_to_remove in logs:
                print('Por favor, escoge uno que este en la lista')
            logs.pop(log_to_remove)
            with open('logs_py.txt', 'w') as f:
                json.dump(logs, f, indent = 4)
            main()
        
        if not logs:
            print('Por favor, crea un log primero.')
            sys.exit(1)

    elif selected == 4:
        print('Adios!')
        sys.exit(1)

    else:
        print('Por favor, introduce un numero valido')
        sys.exit(1)

if __name__ == '__main__':
    main()