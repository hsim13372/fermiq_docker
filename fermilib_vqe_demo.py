
# coding: utf-8

# ## Simulating a variational quantum eigensolver using ProjectQ
# We now demonstrate how one can use both FermiLib and ProjectQ to run a simple VQE example using a Unitary Coupled Cluster ansatz. It demonstrates a simple way to evaluate the energy, optimize the energy with respect to the ansatz and build the corresponding compiled quantum circuit. It utilizes ProjectQ to build and simulate the circuit.

# In[1]:

from numpy import array, concatenate, zeros
from numpy.random import randn
from scipy.optimize import minimize

from fermilib.config import *
from fermilib.utils import *
from fermilib.transforms import jordan_wigner

from projectq.ops import X, All, Measure
from projectq.backends import CommandPrinter, CircuitDrawer


# Here we load H$_2$ from a precomputed molecule file found in the test data directory, and initialize the ProjectQ circuit compiler to a standard setting that uses a first-order Trotter decomposition to break up the exponentials of non-commuting operators. 

# In[6]:

# Load the molecule.
import os
filename = os.path.join(DATA_DIRECTORY, 'H2_sto-3g_singlet_0.7')
molecule = MolecularData(filename=filename)

# Use a Jordan-Wigner encoding, and compress to remove 0 imaginary components
qubit_hamiltonian = jordan_wigner(molecule.get_molecular_hamiltonian())
qubit_hamiltonian.compress()
compiler_engine = uccsd_trotter_engine()

#print(len(qubit_hamiltonian.terms))


# The Variational Quantum Eigensolver (or VQE), works by parameterizing a wavefunction $| \Psi(\theta) \rangle$ through some quantum circuit, and minimzing the energy with respect to that angle, which is defined by
# 
# \begin{align}
# E(\theta) = \langle \Psi(\theta)| H | \Psi(\theta) \rangle
# \end{align}
# 
# To perform the VQE loop with a simple molecule, it helps to wrap the evaluation of the energy into a simple objective function that takes the parameters of the circuit and returns the energy.  Here we define that function using ProjectQ to handle the qubits and the simulation.

# In[7]:

def energy_objective(packed_amplitudes):
    """Evaluate the energy of a UCCSD singlet wavefunction with packed_amplitudes
    Args:
        packed_amplitudes(ndarray): Compact array that stores the unique
            amplitudes for a UCCSD singlet wavefunction.
        
    Returns:
        energy(float): Energy corresponding to the given amplitudes
    """
    # Set Jordan-Wigner initial state with correct number of electrons
    wavefunction = compiler_engine.allocate_qureg(molecule.n_qubits)
    for i in range(molecule.n_electrons):
        X | wavefunction[i]

    # Build the circuit and act it on the wavefunction
    evolution_operator = uccsd_singlet_evolution(packed_amplitudes, 
                                                 molecule.n_qubits, 
                                                 molecule.n_electrons)
    evolution_operator | wavefunction
    compiler_engine.flush()

    # Evaluate the energy and reset wavefunction
    energy = compiler_engine.backend.get_expectation_value(qubit_hamiltonian, wavefunction)
    All(Measure) | wavefunction
    compiler_engine.flush()
    return energy


# While we could plug this objective function into any optimizer, SciPy offers a convenient framework within the Python ecosystem.  We'll choose as starting amplitudes the classical CCSD values that can be loaded from the molecule if desired.  The optimal energy is found and compared to the exact values to verify that our simulation was successful.

# In[ ]:

n_amplitudes = uccsd_singlet_paramsize(molecule.n_qubits, molecule.n_electrons)
initial_amplitudes = [0, 0.05677]
initial_energy = energy_objective(initial_amplitudes)

# Run VQE Optimization to find new CCSD parameters
opt_result = minimize(energy_objective, initial_amplitudes,
                      method="CG", options={'disp':True})

opt_energy, opt_amplitudes = opt_result.fun, opt_result.x
print("\nOptimal UCCSD Singlet Energy: {}".format(opt_energy))
print("Optimal UCCSD Singlet Amplitudes: {}".format(opt_amplitudes))
print("Classical CCSD Energy: {} Hartrees".format(molecule.ccsd_energy))
print("Exact FCI Energy: {} Hartrees".format(molecule.fci_energy))
print("Initial Energy of UCCSD with CCSD amplitudes: {} Hartrees".format(initial_energy))

