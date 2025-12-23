# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent,md
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Qiskit Reference

# %% [markdown]
# **Reference:** [Qiskit Documentation](https://quantum.cloud.ibm.com/docs/en/guides)

# %% [markdown]
# ## Importing

# %%
from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister, Parameter
from qiskit.quantum_info import Statevector, Operator

import numpy as np

# %% [markdown]
# ## Creating Basic Circuits

# %% [markdown]
# **Reference:** [Qiskit Quantum Circuits](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit)
#
# Examples:

# %%
quantum_register = QuantumRegister(size=2, name="x")
ancilla_register = AncillaRegister(
    size=1, name="a"
)  # same as a QuantumRegister, its purpose is only for bookkeeping

quantum_circuit = QuantumCircuit(
    quantum_register, ancilla_register, name="exmaple circuit"
)

# %% [markdown]
# We can now add some gates:

# %%
quantum_circuit.h(quantum_register[0])  # quantum_circuit.h(0)
quantum_circuit.cx(quantum_register[0], quantum_register[1])  # quantum_circuit.cx(0, 1)
quantum_circuit.ccx(
    quantum_register[0], quantum_register[1], ancilla_register[0]
)  # quantum_circuit.ccx(0, 1, 2)
quantum_circuit.y(ancilla_register[0]);  # quantum_circuit.y(12)

# %% [markdown]
# We can see the complex matrix associated to the circuit, using [Operator](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator):

# %%
Operator(quantum_circuit).data

# %% [markdown]
# We can clean up a little:

# %%
print(np.round(Operator(quantum_circuit).data, 3))

# %% [markdown]
# We can print it better with $\LaTeX$:

# %%
Operator(quantum_circuit).draw("latex")

# %% [markdown]
# Although it is usually easy to invert circuits, we can simply use the `inverse` method:

# %%
inverse_quantum_circuit = quantum_circuit.inverse()

# %% [markdown]
# ## Visualization

# %% [markdown]
# We can also [visualize](https://quantum.cloud.ibm.com/docs/en/guides/visualize-circuits) it:

# %%
quantum_circuit.draw()

# %%
inverse_quantum_circuit.draw()

# %% [markdown]
# We have other output styles:

# %%
quantum_circuit.draw(output="mpl")

# %%
quantum_circuit.draw("latex")

# %% [markdown]
# To get the $\LaTeX$ code (for the [qcircuit](https://ctan.org/pkg/qcircuit?lang=en) package, and not the [Quantikz2](https://ctan.org/pkg/quantikz?lang=en)):

# %%
print(quantum_circuit.draw("latex_source"))

# %% [markdown]
# We also have a few [styles](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit):

# %%
quantum_circuit.draw(output="mpl", style="iqp")  # default

# %%
quantum_circuit.draw(output="mpl", style="iqp-dark")

# %%
quantum_circuit.draw(output="mpl", style="clifford")

# %%
quantum_circuit.draw(output="mpl", style="textbook")

# %%
quantum_circuit.draw(output="mpl", style="bw")

# %% [markdown]
# ## States

# %% [markdown]
# We can get the result of a circuit when applied to the initial state $\left| 00 \cdots 0\right\rangle$:

# %%
psi = Statevector(quantum_circuit)
psi

# %% [markdown]
# The result is given as the coefficients in terms of a basis [order](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering#strings) as numbers:
# \begin{align*}
#   0=000_2:& \quad \left| 000 \right\rangle \\
#   1=001_2:& \quad \left| 001 \right\rangle \\
#   2=010_2:& \quad \left| 010 \right\rangle \\
#   3=011_2:& \quad \left| 011 \right\rangle \\
#   \vdots& \\
#   7=111_2:& \quad \left| 111 \right\rangle \\
# \end{align*}

# %% [markdown]
# We can visualize this state better:

# %%
psi.draw("latex")

# %%
print(psi.draw("latex_source"))

# %% [markdown]
# We can also get the correspond probabilities:

# %%
psi.probabilities()

# %%
psi.probabilities_dict()

# %% [markdown]
# We can also create state vectors from strings:

# %%
Statevector.from_label("011").draw("latex")

# %% [markdown]
# We can also use $|+\rangle$ and $|-\rangle$.  So, to get $|+\rangle \otimes |1\rangle \otimes |-\rangle$:

# %%
Statevector.from_label("+1-").draw("latex")

# %% [markdown]
# We can also get state vectors from integers:

# %%
Statevector.from_int(3, dims=16).draw("latex")

# %% [markdown]
# ## Order

# %% [markdown]
# One has to be careful with the order of the qubits:

# %%
two_qubit_x = QuantumCircuit(2)
two_qubit_x.x(0)
two_qubit_x.draw("mpl")

# %% [markdown]
# Let's see what is the output:

# %%
Statevector(two_qubit_x).draw("latex")

# %% [markdown]
# Hence, the input qubits are $|q_1q_0\rangle$, and not $|q_0 q_1\rangle$.  See the video [Why does Qiskit order its qubits the way it does?](https://www.youtube.com/watch?v=EiqHj3_Avps).
#
# We can put the first qubit on top when drawing with `reverse_bits=True`:

# %%
two_qubit_x = QuantumCircuit(2)
two_qubit_x.x(0)
two_qubit_x.draw("mpl", reverse_bits=True)

# %% [markdown]
# Or we can reverse the bits in the circuit itself:

# %%
two_qubit_x = QuantumCircuit(2)
two_qubit_x.x(0)
two_qubit_x = two_qubit_x.reverse_bits()
two_qubit_x.draw("mpl")

# %%
Statevector(two_qubit_x).draw("latex")

# %% [markdown]
# ## Parameters

# %% [markdown]
# We can also add gates that depend on parameters, like rotation gates, using [Parameter](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.Parameter):

# %%
Theta = Parameter(r"$\theta$")

quantum_circuit.rz(Theta, quantum_register[1])
quantum_circuit.draw(output="mpl")

# %% [markdown]
# We can define the parameter to a new circuit:

# %%
new_qc = quantum_circuit.assign_parameters({Theta: np.pi/2})

new_qc.draw("mpl")

# %% [markdown]
# ## Gates:

# %% [markdown]
# We can make a circuit into a gate:

# %%
gate = quantum_circuit.to_gate(label="qc1")

# %% [markdown]
# Let's create a new circuit.

# %%
quantum_register = QuantumRegister(3, name="x")
ancilla_register = AncillaRegister(2, name="a")
quantum_circuit2 = QuantumCircuit(quantum_register, ancilla_register)

quantum_circuit2.x(quantum_register[1])
quantum_circuit2.cz(quantum_register[0], ancilla_register[0])

quantum_circuit2.draw("mpl")

# %% [markdown]
# We can now add the new gate:

# %%
quantum_circuit2.compose(
    gate, [quantum_register[1], quantum_register[2], ancilla_register[0]], inplace=True
)  # note the inplace=True!
quantum_circuit2.draw("mpl")

# %% [markdown]
# We can also create "barriers" in our circuit to separate different pieces of the circuit.  In particular, it prevents Qiskit from moving gates around as well.

# %%
quantum_circuit2.barrier()
quantum_circuit2.h(quantum_register)
quantum_circuit2.barrier()
quantum_circuit2.ccz(quantum_register[1], ancilla_register[0], ancilla_register[1])


quantum_circuit2.draw("mpl")

# %%
