import Graph_Generation
import from_to_binary

bits = from_to_binary.ascii_to_binary("hello world!")

Graph_Generation.generate_graph_NRZ_Polar(bits)
Graph_Generation.generate_graph_ASK(bits)
Graph_Generation.generate_graph_BPSK(bits)
Graph_Generation.generate_graph_QPSK(bits)
Graph_Generation.generate_graph_16QAM(bits)

if __name__ == "__main__":
    from comparacao_ruido import gerar_comparacao

    gerar_comparacao()
