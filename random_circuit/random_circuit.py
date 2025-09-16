import os
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.random import random_circuit
from qiskit.visualization import plot_histogram

#definições
qubits = 10
depth = 1 #quantidade de portas em cada qubit
shots = 1024

#gerando o circuito aleatório
circuit = random_circuit(qubits, depth, measure=True) #measure=True aplica a operação de medição automaticamente

#salva o diagrama do circuito como PNG
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

circuit_filename = os.path.join(output_dir, "random_circuit.png")
circuit.draw(output='mpl', filename=circuit_filename)
print(f"Circuit diagram saved in: {circuit_filename}")

#simulação do Circuito
compiled_circuit = transpile(circuit, AerSimulator()) #adptando o circuito para ser compativel com o AerSimulator
result = AerSimulator().run(compiled_circuit, shots=shots).result() #simulando o circuito
counts = result.get_counts(compiled_circuit) #armazenando as medições no histograma

#salva o histograma como png
histogram_filename = os.path.join(output_dir, "simulation_histogram.png")
plot_histogram(counts, figsize=(15, 10), filename=histogram_filename)
print(f"Simulation histogram saved in: {histogram_filename}")

print("\nResults Analysis: ")

#contador de qubits com valor 1
counts_of_one = [0] * qubits #inicializa o vetor da contagem com '0'

for bitstring, count in counts.items(): #verificando cada indivíduo
    for i in range(qubits): #verificando cada valor do qubit que o indivíduo possue
        if bitstring[qubits - 1 - i] == '1': #invertendo o índice
            counts_of_one[i] += count #se o qubit for 1, soma a quantidade de vezes que ele foi 1

#faz o arredondamento
cutoff = shots / 2
final_state = []
for i in range(qubits):
    count_for_qubit = counts_of_one[i] #indicando quantas vezes apareceu 1 em cada qubit
    print(f"Qubit {i}: Count of '1's = {count_for_qubit}")
    if count_for_qubit > cutoff:
        final_state.append('1')
    else:
        final_state.append('0')

final_state.reverse() #invertendo novamente a sequencia dos qubits
final_bitstring = "".join(final_state) #transformando em string

print(f"\nCutoff frequency: {cutoff}")
print(f"Final rounded state: {final_bitstring}")
