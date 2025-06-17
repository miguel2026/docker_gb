import subprocess
import time
import statistics
import psutil

def parse_mem(mem_str):
    # Exemplo: "21.34MiB / 1GiB"
    used = mem_str.split('/')[0].strip().upper()
    if used.endswith("MIB"):
        return float(used.replace("MIB", ""))
    elif used.endswith("GIB"):
        return float(used.replace("GIB", "")) * 1024
    else:
        return 0

def parse_cpu(cpu_str):
    return float(cpu_str.replace('%', '').strip())

def parse_io(io_str):
    # Exemplo: "1.23MB / 4.56MB"
    read_str, write_str = io_str.split('/')
    def to_mb(s):
        s = s.strip().upper()
        if s.endswith("KB"):
            return float(s.replace("KB", "")) / 1024
        elif s.endswith("MB"):
            return float(s.replace("MB", ""))
        elif s.endswith("GB"):
            return float(s.replace("GB", "")) * 1024
        else:
            return 0
    read_mb = to_mb(read_str)
    write_mb = to_mb(write_str)
    return read_mb + write_mb

def measure_resource_usage(command, duration=10):
    is_docker = (len(command) >= 2 and command[0] == "docker" and command[1] == "exec")
    
    if is_docker:
        container_name = command[2]  # Ex: "docker-postgres-1"
        cpu_samples = []
        mem_samples = []
        io_samples = []
        
        for _ in range(duration):
            result = subprocess.run([
                "docker", "stats", "--no-stream", "--format",
                "{{.CPUPerc}},{{.MemUsage}},{{.BlockIO}}", container_name
            ], capture_output=True, text=True)
            
            if result.returncode != 0 or not result.stdout.strip():
                raise RuntimeError(f"Erro ao coletar métricas do container: {result.stderr}")
            
            cpu_str, mem_str, io_str = result.stdout.strip().split(',')
            cpu_samples.append(parse_cpu(cpu_str))
            mem_samples.append(parse_mem(mem_str))
            io_samples.append(parse_io(io_str))
            
            time.sleep(1)
        
        return {
            'cpu': round(statistics.mean(cpu_samples), 2),
            'memory': round(statistics.mean(mem_samples), 2),
            'io': round(statistics.mean(io_samples), 2)
        }
    else:
        postgres_procs = [p for p in psutil.process_iter(['name']) if 'postgres' in p.info['name']]
        p = postgres_procs[0]
        
        cpu_samples = []
        mem_samples = []
        io_samples = []
        
        for _ in range(duration):
            cpu_samples.append(p.cpu_percent(interval=1))
            mem_samples.append(p.memory_info().rss / 1024**2)  # MB
            io = p.io_counters()
            io_samples.append((io.read_bytes + io.write_bytes) / 1024**2)  # MB/s
        

        print(cpu_samples, mem_samples, io_samples)
        return {
            'cpu': round(statistics.mean(cpu_samples), 2),
            'memory': round(statistics.mean(mem_samples), 2),
            'io': round(statistics.mean(io_samples), 2)
        }
