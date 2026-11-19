# Codificação e modulação de sinais em Python

Projeto para visualizar como uma sequência de bits pode ser representada por sinais. Os gráficos são gerados com Matplotlib, e os cálculos usam NumPy.

## O que você pode visualizar

| Técnica | Como representa os bits |
| --- | --- |
| NRZ polar | Usa o nível −1 para `0` e +1 para `1`. |
| Manchester | Faz uma transição no meio de cada bit: de +1 para −1 no `0` e de −1 para +1 no `1`. |
| ASK | Usa uma senoide para `1` e sinal zero para `0`. |
| BPSK | Usa duas fases da portadora, uma para cada valor de bit. |
| QPSK | Agrupa os bits em pares e usa quatro fases. |
| 16-QAM | Agrupa os bits de quatro em quatro e varia as componentes em fase e em quadratura. |

Apesar do nome do repositório, a versão atual ainda não implementa adição de ruído ao sinal.

## 1. Prepare o ambiente

Você precisa ter **Python 3** e **pip** instalados. O projeto foi verificado com Python 3.12.

Abra um terminal na pasta do projeto e crie um ambiente virtual:

```bash
python -m venv .venv
```

Se o comando `python` não estiver disponível no Linux ou macOS, use `python3`.

Ative o ambiente conforme o seu sistema:

**Linux ou macOS:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as duas dependências:

```bash
python -m pip install numpy matplotlib
```

## 2. Execute o exemplo

Com o ambiente virtual ativo, execute:

```bash
python main.py
```

O programa usa a sequência `1101001110010110` e exibe cinco gráficos nesta ordem: ASK, BPSK, QPSK, 16-QAM e NRZ polar. Em uma execução comum pelo terminal, feche a janela de cada gráfico para abrir o próximo.

O exemplo não pede dados pelo terminal. Para trocar a sequência, edite os valores passados às funções em `main.py`.

## 3. Gere um gráfico com seus próprios bits

Crie um arquivo chamado `exemplo.py` na mesma pasta de `main.py`:

```python
import Graph_Generation

bits = "1010101011001100"

Graph_Generation.generate_graph_manchester(bits)
```

Execute com:

```bash
python exemplo.py
```

Para escolher outra técnica, substitua a última linha por uma destas chamadas:

```python
Graph_Generation.generate_graph_NRZ_Polar(bits)
Graph_Generation.generate_graph_ASK(bits)
Graph_Generation.generate_graph_BPSK(bits)
Graph_Generation.generate_graph_QPSK(bits)
Graph_Generation.generate_graph_16QAM(bits)
```

### Regras para a entrada

- Passe uma string com **pelo menos 16 bits**, usando apenas `0` e `1`, sem espaços.
- No QPSK, se a quantidade de bits for ímpar, o programa acrescenta um `0` ao final.
- No 16-QAM, o programa acrescenta zeros ao final até completar um múltiplo de quatro bits.
- Se a entrada for inválida, a função de gráfico retorna uma mensagem de erro em inglês e não abre o gráfico. Para ler a mensagem, use `print(Graph_Generation.generate_graph_ASK(bits))`. Quando a entrada é válida, o retorno é `None`.

## Conversão entre texto e binário

O módulo `from_to_binary.py` oferece funções auxiliares. Exemplo com texto ASCII:

```python
from from_to_binary import ascii_to_binary, binary_to_ascii

bits = ascii_to_binary("Oi")
print(bits)                   # 0100111101101001
print(binary_to_ascii(bits))   # Oi
```

Para uma conversão de ida e volta previsível, use texto ASCII, sem acentos ou emojis, e sequências binárias com grupos completos de oito bits. Essas funções não fazem codificação UTF-8.

## Organização dos arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Executa os cinco gráficos de exemplo. |
| `Codification.py` | Gera os sinais Manchester e NRZ polar. |
| `Modulation.py` | Gera os sinais ASK, BPSK, QPSK e 16-QAM. |
| `Graph_Generation.py` | Valida a entrada e exibe os gráficos. |
| `from_to_binary.py` | Converte texto em bits e bits em texto. |

## Problemas comuns

- **`ModuleNotFoundError` para `numpy` ou `matplotlib`:** ative o ambiente virtual e execute novamente `python -m pip install numpy matplotlib`.
- **O gráfico não aparece:** a exibição em janelas precisa de um ambiente gráfico e de um backend interativo do Matplotlib. Em servidores ou terminais sem interface gráfica, salve a figura em um arquivo substituindo `plt.show()` por `plt.savefig("grafico.png")` na função desejada em `Graph_Generation.py`.
- **Nenhum gráfico aparece com uma nova sequência:** confira se ela contém apenas `0` e `1` e tem pelo menos 16 bits. Imprima o retorno da função para conferir a mensagem de validação.
