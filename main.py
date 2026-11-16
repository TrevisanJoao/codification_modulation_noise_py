import from_to_binary
import Codification
import Modulation
import Graph_Generation

def main():
    # Example usage of the functions
    Graph_Generation.generate_graph_ASK("1101001110010110")
    Graph_Generation.generate_graph_BPSK("1101001110010110")
    Graph_Generation.generate_graph_QPSK("1101001110010110")
    Graph_Generation.generate_graph_16QAM("1101001110010110")
    Graph_Generation.generate_graph_NRZ_Polar("1101001110010110")

if __name__ == "__main__":
    main()