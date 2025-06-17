import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

docker_df = pd.read_csv("../results/docker_results.csv")
native_df = pd.read_csv("../results/native_results.csv")

combined = pd.concat([docker_df.assign(env='Docker'),
                      native_df.assign(env='Local')])

sns.set(style="whitegrid")

def plot_metric(metric):
    plt.figure(figsize=(8,5))
    sns.barplot(x='env', y=metric, data=combined)
    plt.title(f'Comparação de {metric}')
    plt.savefig(f'../results/{metric}_comparison.png')
    plt.close()

for metric in ['start_time', 'memory_mb', 'cpu_percent', 'io_mb_s', 'latency_ms']:
    plot_metric(metric)
print("hey")