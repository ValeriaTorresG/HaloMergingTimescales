import subprocess, os, time

def run_script():
    command = ['python3', 'script2.py']
    files = [f for f in os.listdir('/net/hypernova/data2/BOOMPJE/') if f.startswith(f'merging_')]
    for f in files:
        try:
            t = time.time()
            subprocess.run(['python3', 'scripts/qv_anim.py', f'/net/hypernova/data2/BOOMPJE/{f}'], check=True, capture_output=True, text=True)
            print(f'{f}: {round((time.time()-t)/60, 4)}')
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f'{result.stdout}, {result.stderr}, {f}: {round((time.time()-t)/60, 4)}')
            
        except subprocess.CalledProcessError as e:
            print('Error: ', e)

if __name__ == "__main__":
    run_script()