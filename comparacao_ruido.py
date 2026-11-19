"""Comparação em banda base com detecção coerente e ruído branco gaussiano."""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import Codification
import Modulation


MODULACOES = {
    "ASK": (1, Modulation.generate_ASK_modulated_signal),
    "BPSK": (1, Modulation.generate_BPSK_modulated_signal),
    "QPSK": (2, Modulation.generate_QPSK_modulated_signal),
    "16-QAM": (4, Modulation.generate_16QAM_modulated_signal),
}
CODIGOS = {
    "NRZ polar": (1, Codification.generate_nrz_polar_signal),
    "Manchester": (2, Codification.generate_manchester_signal),
}
NIVEIS_DB = range(-4, 13, 2)
NIVEIS_CONSTELACAO = (0, 6)


def alfabeto(codigo, modulacao):
    """Palavras válidas e suas sequências de símbolos I/Q, com Eb médio unitário."""
    chips_por_bit, codificar = CODIGOS[codigo]
    chips_por_simbolo, modular = MODULACOES[modulacao]
    largura = max(1, chips_por_simbolo // chips_por_bit)
    deslocamentos = np.arange(largura - 1, -1, -1)
    palavras = (np.arange(2**largura)[:, None] >> deslocamentos) & 1

    # Projeta uma vez as formas de onda do projeto nas referências da portadora.
    ondas = np.array([modular(codificar(p)) for p in palavras])
    simbolos_por_palavra = largura * chips_por_bit // chips_por_simbolo
    ondas = ondas.reshape(len(palavras), simbolos_por_palavra, -1)
    fase = 2 * np.pi * 5 * np.arange(ondas.shape[-1]) / ondas.shape[-1]
    referencia = (np.exp(-1j * fase) if modulacao == "16-QAM"
                  else np.sin(fase) + 1j * np.cos(fase))
    pontos = 2 * np.mean(ondas * referencia, axis=-1)
    pontos = pontos.round(12)  # Elimina resíduos numéricos da projeção.
    energia = np.mean(np.sum(abs(pontos)**2, axis=1))
    return palavras, pontos * np.sqrt(largura / energia)


def detectar(recebidos, alfabeto_iq):
    # A distância inclui os dois símbolos quando Manchester ocupa dois intervalos.
    distancias = np.stack([
        np.sum(abs(recebidos - candidato)**2, axis=1) for candidato in alfabeto_iq
    ], axis=1)
    return np.argmin(distancias, axis=1)


def desenhar_nuvem(ax, recebidos, enviados, decididos, ideais):
    # Os pontos são consecutivos para preservar a frequência real dos erros.
    amostra = recebidos.ravel()[:800]
    erros = enviados.ravel()[:800] != decididos.ravel()[:800]
    ax.scatter(amostra[~erros].real, amostra[~erros].imag, s=8, alpha=.42,
               color="#16718a", label="Símbolo correto")
    ax.scatter(amostra[erros].real, amostra[erros].imag, marker="x", s=20,
               linewidths=.9, color="#bd391d", label="Símbolo errado")
    ax.scatter(ideais.real, ideais.imag, marker="D", s=38, color="white",
               edgecolors="black", linewidths=1.4, label="Posição ideal")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(alpha=.18)
    ax.set_axisbelow(True)
    return f"{erros.sum()} erros em {len(amostra)} símbolos exibidos"


def gerar_comparacao(pasta=Path("comparacao_ruido")):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(2026)
    bits = rng.integers(0, 2, 40000)
    linhas = []
    fig_ber, paineis = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True,
                                    layout="constrained")
    fig_ber.suptitle("Erros por bit de informação em canal AWGN")
    for ax_ber, codigo in zip(paineis, CODIGOS):
        fig, eixos = plt.subplots(4, 2, figsize=(9, 13), sharex="row", sharey="row",
                                  layout="constrained")
        fig.suptitle(f"Constelações com {codigo}  ·  canal AWGN")
        for modulacao, par, marcador in zip(MODULACOES, eixos, "os^D"):
            palavras, pontos = alfabeto(codigo, modulacao)
            largura = palavras.shape[1]
            indices = bits.reshape(-1, largura) @ (2 ** np.arange(largura - 1, -1, -1))
            enviados = pontos[indices]
            taxas = []
            for db in NIVEIS_DB:
                # Eb = 1. Cada componente do ruído tem variância N0/2.
                sigma = np.sqrt(0.5 * 10**(-db / 10))
                ruido = rng.normal(size=enviados.shape) + 1j * rng.normal(size=enviados.shape)
                recebidos = enviados + sigma * ruido
                escolhas = detectar(recebidos, pontos)
                erros = np.count_nonzero(palavras[escolhas].ravel() != bits)
                taxas.append(erros / len(bits))
                linhas.append((codigo, modulacao, db, len(bits), erros, taxas[-1]))
                if db in NIVEIS_CONSTELACAO:
                    ax = par[NIVEIS_CONSTELACAO.index(db)]
                    contagem = desenhar_nuvem(ax, recebidos, enviados, pontos[escolhas],
                                              np.unique(pontos))
                    ax.set_title(f"{modulacao}   ·   {db} dB\n{contagem}", fontsize=10)
                    ax.set_xlabel("Em fase (I)")
                    ax.set_ylabel("Quadratura (Q)")
            ax_ber.plot(NIVEIS_DB, taxas, marker=marcador, markersize=5,
                        markerfacecolor="none", label=modulacao)
        ax_ber.set_title(codigo)
        ax_ber.set_xlabel("Energia por bit / densidade de ruído, Eb/N₀ (dB)")
        ax_ber.set_yscale("symlog", linthresh=1 / len(bits))
        ax_ber.set_ylim(bottom=0)
        ax_ber.set_xticks(list(NIVEIS_DB))
        ax_ber.grid(alpha=.25)
        ax_ber.legend()
        handles, labels = eixos[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="outside lower center", ncols=3)
        fig.savefig(pasta / f"constelacao_{codigo.lower().replace(' ', '_')}.png", dpi=140)
        plt.close(fig)
    paineis[0].set_ylabel("BER (bits errados / bits transmitidos)")
    fig_ber.savefig(pasta / "ber_por_db.png", dpi=150)
    plt.close(fig_ber)
    with (pasta / "erros_por_db.csv").open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(("codificacao", "modulacao", "eb_n0_db", "bits", "erros", "ber"))
        escritor.writerows(linhas)
    print(f"Gráficos e contagens de erros em {pasta.resolve()}")


if __name__ == "__main__":
    gerar_comparacao()
