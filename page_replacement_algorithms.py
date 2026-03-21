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
