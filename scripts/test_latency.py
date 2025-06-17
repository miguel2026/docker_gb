import psycopg2
import time
import statistics

def measure_latency(host, port, user, password, dbname, queries=20):
    times = []
    try:
        conn = psycopg2.connect(
            host=host, port=port,
            user=user, password=password, dbname=dbname
        )
        cursor = conn.cursor()
        for _ in range(queries):
            start = time.time()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            times.append((time.time() - start) * 1000)  # ms
        cursor.close()
        conn.close()
        return round(statistics.mean(times), 2)
    except Exception as e:
        print("Erro de latência:", e)
        return -1