import os
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

#definições
num_qubits = 10
num_shots = 1024
#quantidade portas lógicas em cada qubit
depth = 3

#Gera o circuito aleátorio
qc = QuantumCircuit(num_qubits, num_qubits)
single_qubit_gates = ['h', 'x', 'y', 'z', 't', 'rx', 'ry', 'rz']
multi_qubit_gates = ['cx', 'cz', 'swap']
for _ in range(depth):
    for i in range(num_qubits):
        #Escolhendo uma porta lógica aleátoria
        gate_type = np.random.choice(single_qubit_gates)
        
        if gate_type == 'h': qc.h(i)
        elif gate_type == 'x': qc.x(i)
        elif gate_type == 'y': qc.y(i)
        elif gate_type == 'z': qc.z(i)
        elif gate_type == 't': qc.t(i)
        elif gate_type in ['rx', 'ry', 'rz']:
            angle = np.random.uniform(0, 2 * np.pi)
            if gate_type == 'rx': qc.rx(angle, i)
            elif gate_type == 'ry': qc.ry(angle, i)
            elif gate_type == 'rz': qc.rz(angle, i)

    #Cria o emaranhamento
    if num_qubits > 1:
        entangler = np.random.choice(multi_qubit_gates)
        q1, q2 = np.random.choice(range(num_qubits), 2, replace=False)
        if entangler == 'cx': qc.cx(q1, q2)
        elif entangler == 'cz': qc.cz(q1, q2)
        elif entangler == 'swap': qc.swap(q1, q2)

    # Separa visualmente as portas
    qc.barrier()
# Adiciona medição em todos os qubits no final
qc.measure(range(num_qubits), range(num_qubits))
# Atribui o circuito gerado à variável principal
circuit = qc

#salva o diagrama do circuito como PNG
script_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(script_dir, "output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
circuit_filename = os.path.join(output_dir, "random_circuit.png")
circuit.draw(output='mpl', filename=circuit_filename)
print(f"Circuit diagram saved in: {circuit_filename}")

#simulação do Circuito
compiled_circuit = transpile(circuit, AerSimulator())
result = AerSimulator().run(compiled_circuit, shots=num_shots).result()
counts = result.get_counts(compiled_circuit)

#salva o histograma como png
histogram_filename = os.path.join(output_dir, "simulation_histogram.png")
plot_histogram(counts, figsize=(15, 10), filename=histogram_filename)
print(f"Simulation histogram saved in: {histogram_filename}")

print("\nResults Analysis:")

# Definição do intervalo de mapeamento [a, b]
a = 0
b = 1
max_int_value = 2**num_qubits - 1

#Transforma os resultados em inteiro para converter e arredondar.
for bitstring, count in counts.items():
    x = int(bitstring, 2)
    mapped_value = (x / max_int_value) * (b - a) + a
    rounded_value = round(mapped_value)
    
    print(f"Bitstring: {bitstring} -> Mapped: {mapped_value:.4f} -> Rounded: {rounded_value} (appeared {count} times)")