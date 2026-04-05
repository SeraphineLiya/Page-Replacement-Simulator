# Import parts 1 and 2
from algorithms import fifo_page_replacement, lru_page_replacement, clock_page_replacement

def run_simulation(input_data):
    """
    Part 3: Integration and Flow
    """
    # extraction of input parameters
    algorithm = input_data.get("algorithm")
    frames = input_data.get("frames")
    references = input_data.get("references")
    trace = input_data.get("trace", False)

    # routing: decides which function to call based on the input.
    if algorithm == "FIFO":
        sim_result = fifo_page_replacement(frames, references, trace)
    elif algorithm == "LRU":
        sim_result = lru_page_replacement(frames, references, trace)
    elif algorithm == "Clock":
        sim_result = clock_page_replacement(frames, references, trace)
    else:
        raise ValueError(f"Algoritmo inválido ou não suportado: {algorithm}")

    # format the output to match what the spell checker expects.
    output_data = {
        "algorithm": algorithm,
        "frames": frames,
        "faults": sim_result["faults"],
        "hits": sim_result["hits"],
        "final_frames": sim_result["final_frames"]
    }

    # only add the "trace" if it has been requested and generated.
    if "trace" in sim_result:
        output_data["trace"] = sim_result["trace"]

    return output_data