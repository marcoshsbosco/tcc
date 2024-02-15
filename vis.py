import matplotlib.pyplot as plt


def plot(data):
    fig, ax = plt.subplots()

    ax.set_xlabel("Gerações decorridas")
    ax.set_ylabel("Melhor aptidão")

    for k, v in data.items():
        ax.plot(v)

    ax.legend()

    fig.savefig(f'result.png')

def plot_nutrients(data):
    fig, ax = plt.subplots(figsize=(12, 6))

    nutrients = data.keys()
    values = data.values()

    # values = [min(1, x) for x in values]

    ax.barh(list(nutrients), values)

    ax.set_ylabel("Razão nutriente/IDR")
    ax.set_title("Quantidade de nutrientes relativo ao seus valores de IDR")
    ax.set_xlim([None, 2])

    fig.savefig('resultbars.png')

