import time
import subprocess
import psutil
import requests
import csv
import os
import statistics
import psycopg2
from pathlib import Path
import pandas as pd

# bibliotecas pessoais

from test_latency import measure_latency
from test_memory_cpu_io import measure_resource_usage
from test_start_time import measure_start_time, measure_start_time_windows

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR = str(RESULTS_DIR)
REPEAT = 5  # número de execuções para média
os.environ["PGPASSWORD"] = "1234" # senha do pspql

def measure_density(command, max_instances=10):
    count = 0
    processes = []
    for _ in range(max_instances):
        try:
            p = subprocess.Popen(command, stdout=subprocess.DEVNULL)
            processes.append(p)
            time.sleep(0.5)
            count += 1
        except Exception:
            break
    for p in processes:
        p.terminate()
    return count

def run_all_tests(env_name, dockerized):
    print(f"Iniciando testes para: {env_name}")

    docker_cmd_up = ["docker-compose", "up", "-d"]
    docker_cmd_down = ["docker-compose", "down"]
    cwd = Path(__file__).resolve().parent.parent / "docker"
    cwd = str(cwd)

    if dockerized:
        start_time = measure_start_time(docker_cmd_up, docker_cmd_down, cwd)
        subprocess.run(docker_cmd_up, cwd=cwd, stdout=subprocess.DEVNULL)
        time.sleep(5)
        cmd = cmd = ["docker", "exec", "docker-postgres-1", "psql", "-U", "postgres", "-d", "testdb", "-c", "SELECT 1;"]

    else:
        win_service_name = "postgresql-x64-17"
        start_cmd = ["net", "start", win_service_name]
        stop_cmd = ["net", "stop", win_service_name]
        start_time = measure_start_time_windows(start_cmd, stop_cmd)
        time.sleep(5)
        # altere a primeira parte para onde fica o seu pqsql.exe no seu computador ou deixe somente psql se tiver no PATH
        cmd = [r"C:\Program Files\PostgreSQL\17\bin\psql.exe", "-U", "postgres", "-d", "testdb", "-c", "SELECT 1;"]

    # Recursos
    resources = measure_resource_usage(cmd)

    # Latência
    latency = measure_latency(
        host="localhost", port=5432,
        user="postgres", password="1234", dbname="testdb"
    )
    # Densidade
    density = measure_density(cmd)

    if dockerized:
        subprocess.run(docker_cmd_down, cwd=cwd)
    else:
        subprocess.run(stop_cmd, stdout=subprocess.DEVNULL)

    return {
        "start_time": start_time,
        "memory_mb": resources['memory'],
        "cpu_percent": resources['cpu'],
        "io_mb_s": resources['io'],
        "latency_ms": latency,
        "density": density
    }

def save_results(filename, data):
    filepath = os.path.join(RESULTS_DIR, filename)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    df = pd.DataFrame([data])  # transforma o dicionário em um DataFrame de uma linha

    df.to_csv(filepath, mode="w", index=False, header=True)


if __name__ == "__main__":
    docker_data = run_all_tests("Docker", dockerized=True)
    save_results("docker_results.csv", docker_data)

    native_data = run_all_tests("Local", dockerized=False)
    save_results("native_results.csv", native_data)

    print("\nTestes completos! Resultados salvos na pasta 'results'.")
