import subprocess
from multiprocessing import Process, Manager, Event

def run_script(script_name, results, dependencies, error_event):
    try:
        if dependencies:
            # Espera até que todas as dependências estejam disponíveis
            for dep in dependencies:
                while dep not in results:
                    if error_event.is_set():
                        return
        result = subprocess.run(['python', script_name], capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            error_event.set()
            results[script_name] = f"Error: {result.stderr.strip()}"
        else:
            results[script_name] = result.stdout.strip()
    except Exception as e:
        error_event.set()
        results[script_name] = f"Exception: {str(e)}"

def main():
    manager = Manager()
    results = manager.dict()
    error_event = Event()
    
    # Lista de scripts com suas dependências, na ordem correta
    scripts = [
        {'name': 'allow_df.py', 'dependencies': []},
        {'name': 'get_date.py', 'dependencies': ['allow_df.py']},
        {'name': 'get_horario.py', 'dependencies': ['allow_df.py']},
        {'name': 'query_rds1.py', 'dependencies': ['get_DATE.py']},
       # {'name': 'comp1.py', 'dependencies': ['query_rds1.py', 'cnx_bucket.py']},
       # {'name': 'send_tomb1.py', 'dependencies': ['get_DATE.py']},
       # {'name': 'query_ver1.py', 'dependencies': ['cnx_rds1.py', 'get_DATE.py']}#
    ]
    
    processes = []
    
    for script in scripts:
        p = Process(target=run_script, args=(script['name'], results, script['dependencies'], error_event))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print("Results from scripts:")
    for script_name, result in results.items():
        print(f"{script_name}: {result}")
        if "Error:" in result or "Exception:" in result:
            print(f"Execution stopped due to an error in script: {script_name}")
            break

if __name__ == "__main__":
    main()
