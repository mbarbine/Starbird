import subprocess
from settings import *
def quantum_decision():
    # Compile and execute the CUDA Q decision kernel
    subprocess.run(['nvcc', '--cuda', 'quantum_decision.cu', '-o', 'quantum_decision'])
    result = subprocess.run(['./quantum_decision'], capture_output=True, text=True)

    # Return the decision
    return int(result.stdout.strip())

def random_dark_side_event():
    decision = quantum_decision()
    if decision == 1:
        # Dark Side event
        activate_force_push(obstacles)
    else:
        # Light Side bonus
        activate_force_shield(bird)
