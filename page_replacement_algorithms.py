def fifo_page_replacement(frame_count, references, trace=False):
    if frame_count <= 0:
        result = {
            "faults": len(references),
            "hits": 0,
            "final_frames": []
        }
        if trace:
            result["trace"] = [
                {"page": page, "result": "FAULT", "frames": []}
                for page in references
            ]
        return result

    frames = []
    hits = 0
    faults = 0
    replace_index = 0
    trace_steps = []

    for page in references:

        if page in frames:
            hits += 1
            access_result = "HIT"

        else:
            faults += 1
            access_result = "FAULT"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames[replace_index] = page
                replace_index = (replace_index + 1) % frame_count

        if trace:
            trace_steps.append({
                "page": page,
                "result": access_result,
                "frames": frames.copy()
            })

    result = {
        "faults": faults,
        "hits": hits,
        "final_frames": frames
    }

    if trace:
        result["trace"] = trace_steps

    return result


def lru_page_replacement(frame_count, references, trace=False):
    if frame_count <= 0:
        result = {
            "faults": len(references),
            "hits": 0,
            "final_frames": []
        }
        if trace:
            result["trace"] = [
                {"page": page, "result": "FAULT", "frames": []}
                for page in references
            ]
        return result

    frames = []
    hits = 0
    faults = 0
    last_used = {}
    trace_steps = []

    for time, page in enumerate(references):

        if page in frames:
            hits += 1
            access_result = "HIT"
            last_used[page] = time

        else:
            faults += 1
            access_result = "FAULT"

            if len(frames) < frame_count:
                frames.append(page)

            else:
                victim_page = min(frames, key=lambda p: (last_used[p], p))
                victim_index = frames.index(victim_page)

                frames[victim_index] = page
                del last_used[victim_page]

            last_used[page] = time

        if trace:
            trace_steps.append({
                "page": page,
                "result": access_result,
                "frames": frames.copy()
            })

    result = {
        "faults": faults,
        "hits": hits,
        "final_frames": frames
    }

    if trace:
        result["trace"] = trace_steps

    return result

def clock_page_replacement(frame_count, references, trace=False):
    # If there are no frames, every page access is a fault
    if frame_count <= 0:
        result = {
            "faults": len(references),
            "hits": 0,
            "final_frames": []
        }
        if trace:
            result["trace"] = [
                {
                    "page": page,
                    "result": "FAULT",
                    "frames": [],
                    "reference_bits": [],
                    "pointer": 0
                }
                for page in references
            ]
        return result

    # Stores the pages currently loaded in memory
    frames = []

    # Stores the reference bit for each frame
    reference_bits = []

    # Counts hits and faults
    hits = 0
    faults = 0

    # Acts like the clock hand / circular pointer
    pointer = 0

    # Stores step-by-step trace info if needed
    trace_steps = []

    # Go through each page in the reference string
    for page in references:

        # If the page is already in memory, it is a hit
        if page in frames:
            hits += 1
            access_result = "HIT"

            # Set its reference bit to 1 since it was just used
            page_index = frames.index(page)
            reference_bits[page_index] = 1

        else:
            # If page is not in memory, it is a fault
            faults += 1
            access_result = "FAULT"

            # If there is still room, just add the page
            if len(frames) < frame_count:
                frames.append(page)
                reference_bits.append(1)

            else:
                # Memory is full, so use the Clock replacement rule
                # Keep moving until we find a page with reference bit 0
                while reference_bits[pointer] == 1:
                    # Give this page a second chance by changing 1 to 0
                    reference_bits[pointer] = 0

                    # Move pointer to the next frame in a circle
                    pointer = (pointer + 1) % frame_count

                # Replace the page at the pointer
                frames[pointer] = page
                reference_bits[pointer] = 1

                # Move pointer forward after replacement
                pointer = (pointer + 1) % frame_count

        # Save trace information after each page access
        if trace:
            trace_steps.append({
                "page": page,
                "result": access_result,
                "frames": frames.copy(),
                "reference_bits": reference_bits.copy(),
                "pointer": pointer
            })

    # Final result
    result = {
        "faults": faults,
        "hits": hits,
        "final_frames": frames
    }

    # Add trace if requested
    if trace:
        result["trace"] = trace_steps

    return result