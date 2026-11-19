# Codificação e modulação de sinais em Python

Projeto para visualizar como uma sequência de bits pode ser representada por sinais. Os gráficos são gerados com Matplotlib, e os cálculos usam NumPy.

## Video demonstrativo

https://github.com/user-attachments/assets/3b10659a-fb76-4d31-bc2f-e61848909ceb

## O que você pode visualizar

| Técnica | Como representa os bits |
| --- | --- |
| NRZ polar | Usa o nível −1 para `0` e +1 para `1`. |
| Manchester | Faz uma transição no meio de cada bit: de +1 para −1 no `0` e de −1 para +1 no `1`. |
| ASK | Usa uma senoide para `1` e sinal zero para `0`. |
| BPSK | Usa duas fases da portadora, uma para cada valor de bit. |
| QPSK | Agrupa os bits em pares e usa quatro fases. |
| 16-QAM | Agrupa os bits de quatro em quatro e varia as componentes em fase e em quadratura. |

O projeto simula ruído branco gaussiano aditivo (AWGN) e ruído em rajadas. A comparação por dB usa AWGN.

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

O programa transmite a mensagem `Hello World!` com NRZ polar e BPSK e imprime a mensagem recuperada e a taxa de erro para AWGN e rajadas.

### Compare os erros e as constelações

Rode `python comparacao_ruido.py` para gerar os resultados na pasta `comparacao_ruido/`. Use `python exemplo.py` para ver também as formas de onda no tempo.

| Arquivo | O que observar |
| --- | --- |
| `ber_por_db.png` | Cada painel mostra uma codificação. As quatro curvas comparam a fração de bits de informação recebidos com erro, de −4 a 12 dB. Zero indica que todos os 40.000 bits daquela medição foram recuperados. |
| `constelacao_nrz_polar.png` e `constelacao_manchester.png` | Para cada modulação, compare os primeiros 800 símbolos a 0 e 6 dB na mesma escala. Os losangos indicam as posições ideais, os pontos azuis são acertos e as cruzes vermelhas são erros de símbolo. Um erro de símbolo pode afetar mais de um bit. |
| `erros_por_db.csv` | Contagens de bits transmitidos e errados e BER para cada combinação de codificação, modulação e nível de ruído. |

O eixo horizontal usa Eb/N₀, com energia média unitária por **bit de informação** em todas as combinações. As mesmas entradas aleatórias são usadas em toda a comparação, com semente fixa para reproduzir os gráficos. O ruído é gaussiano independente nos eixos I e Q, com variância N₀/2 em cada eixo. [Relação entre energia por bit e por símbolo](https://www.mathworks.com/help/comm/ug/awgn-channel.html).

O simulador extrai as posições I/Q das formas de onda do projeto. O receptor escolhe a sequência válida mais próxima das amostras recebidas. No Manchester, os dois níveis que representam cada bit são avaliados juntos. Isso restringe as posições possíveis em QPSK e 16-QAM e explica por que as nuvens podem ter menos centros. As curvas comparam erros para a mesma energia por bit, sem igualar a taxa de transmissão.

## 3. Gere um gráfico com seus próprios bits

Para gerar um gráfico isolado, salve o trecho abaixo em `meu_grafico.py`, na mesma pasta de `main.py`:

```python
import Graph_Generation

bits = "1010101011001100"

Graph_Generation.generate_graph_manchester(bits)
```

Execute com:

```bash
python meu_grafico.py
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
| `main.py` | Compara uma transmissão BPSK sob AWGN e ruído em rajadas. |
| `Codification.py` | Gera os sinais Manchester e NRZ polar. |
| `Modulation.py` | Gera os sinais ASK, BPSK, QPSK e 16-QAM. |
| `Graph_Generation.py` | Valida a entrada e exibe os gráficos. |
| `from_to_binary.py` | Converte texto em bits e bits em texto. |

## Problemas comuns

- **`ModuleNotFoundError` para `numpy` ou `matplotlib`:** ative o ambiente virtual e execute novamente `python -m pip install numpy matplotlib`.
- **O gráfico não aparece em uma janela:** a exibição em janelas precisa de um ambiente gráfico e de um backend interativo do Matplotlib. Quando o backend é `Agg`, as funções de gráfico salvam automaticamente arquivos PNG na pasta de execução e mostram o nome no terminal: `manchester.png`, `nrz_polar.png`, `ask.png`, `bpsk.png`, `qpsk.png` ou `16qam.png`. Uma nova execução substitui o arquivo correspondente.
- **Nenhum gráfico aparece com uma nova sequência:** confira se ela contém apenas `0` e `1` e tem pelo menos 16 bits. Imprima o retorno da função para conferir a mensagem de validação.
