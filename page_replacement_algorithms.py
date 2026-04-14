def fifo_page_replacement(frame_count, references, trace=False):
    #This function simulates the FIFO page replacement algorithm
    #FIFO means First-In, First-Out
    #That means when memory is full, the page that entered first is the one removed first
    #If the number of frames is 0 or less, memory cannot hold any pages
    #So every page reference will automatically be a fault
    if frame_count <= 0:
        result = {
            "faults": len(references), # every reference becomes a fault
            "hits": 0, # no page can ever already be in memory
            "final_frames": [] # memory stays empty
        }
        #If trace is turned on, we store the result of every step
        if trace:
            result["trace"] = [
                {"page": page, "result": "FAULT", "frames": []}
                for page in references
            ]
        return result

    #frames stores the current pages in memory
    frames = []
    #hits counts how many times the page was already in memory
    hits = 0
    #faults counts how many times the page was not in memory
    faults = 0
    #replace_inde tells us which frame position should be replaced next
    #In FIFO, once memory is full, we replace pages in the same order they entered
    replace_index = 0
    #trace_steps will store step-by-step memory states is trace=True
    trace_steps = []
    #Go through each page in the reference sequence one by one
    for page in references:
        # Check if the current page is already in memory
        if page in frames:
            # If yes, it is a hit
            hits += 1
            access_result = "HIT"

        else:
            # If not, it is a fault
            faults += 1
            access_result = "FAULT"

            # If there is still space in memory, just add the page
            if len(frames) < frame_count:
                frames.append(page)
            else:
                # Memory is full, so replace the oldest page using replace_index
                frames[replace_index] = page

                # Move replace_index forward in circular order
                replace_index = (replace_index + 1) % frame_count

        # Save current step if trace is enabled
        if trace:
            trace_steps.append({
                "page": page,
                "result": access_result,
                "frames": frames.copy()
            })

    # Store final results after processing all pages
    result = {
        "faults": faults,
        "hits": hits,
        "final_frames": frames
    }

    # Attach trace if needed
    if trace:
        result["trace"] = trace_steps

    return result


def lru_page_replacement(frame_count, references, trace=False):
    # LRU means Least Recently Used
    # This algorithm replaces the page that has not been used for the longest time

    # If there are no frames, every reference is a fault
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

    # Stores current pages in memory
    frames = []
    # Count of hits
    hits = 0
    # Count of faults
    faults = 0
    # Dictionary to track last time each page was used
    last_used = {}
    # Stores step-by-step trace
    trace_steps = []

    # enumerate gives both index (time) and page
    for time, page in enumerate(references):

        # Check if page is already in memory
        if page in frames:
            # It is a hit
            hits += 1
            access_result = "HIT"

            # Update last used time since page was just accessed
            last_used[page] = time

        else:
            # It is a fault
            faults += 1
            access_result = "FAULT"

            # If there is space, just add the page
            if len(frames) < frame_count:
                frames.append(page)

            else:
                # Find the least recently used page
                # min() chooses the page with smallest last_used value
                # If tie, smaller page number is chosen
                victim_page = min(frames, key=lambda p: (last_used[p], p))

                # Find its index in frames
                victim_index = frames.index(victim_page)

                # Replace it with the new page
                frames[victim_index] = page

                # Remove old page from last_used since it's no longer in memory
                del last_used[victim_page]

            # Update last used time for the new page
            last_used[page] = time

        # Save current step if trace is enabled
        if trace:
            trace_steps.append({
                "page": page,
                "result": access_result,
                "frames": frames.copy()
            })

    # Final result after processing all references
    result = {
        "faults": faults,
        "hits": hits,
        "final_frames": frames
    }

    # Attach trace if needed
    if trace:
        result["trace"] = trace_steps

    return result

def clock_page_replacement(frame_count, references, trace=False):
    #This function simulates the Clock (Second-Chance) page replacement algorithm
    #It uses a circular pointer and reference bits to give pages a second chance before replacement
    
    #If the number of frames is 0 or less, memory cannot hold any pages
    if frame_count <= 0:
        result = {"faults": len(references), "hits": 0, "final_frames": []}
        #If trace is turned on, we store the result of every step
        if trace:
            result["trace"] = [{"page": page, "result": "FAULT", "frames": [], "reference_bits": [], "pointer": 0} for page in references]
        return result

    #frames stores the current pages in memory
    frames = []
    #reference_bits stores a 1 or 0 for each page in memory
    reference_bits = []
    #hits counts how many times the page was already in memory
    hits = 0
    #faults counts how many times the page was not in memory
    faults = 0
    #pointer acts like a clock hand moving through the frames
    pointer = 0
    #trace_steps will store step-by-step memory states if trace=True
    trace_steps = []

    #Go through each page in the reference sequence one by one
    for page in references:
        # Check if the current page is already in memory
        if page in frames:
            # If yes, it is a hit
            hits += 1
            access_result = "HIT"
            
            # Set its reference bit to 1 since it was just used
            page_index = frames.index(page)
            reference_bits[page_index] = 1
            
        else:
            # If not, it is a fault
            faults += 1
            access_result = "FAULT"
            
            # If there is still space in memory, just add the page and set its bit to 1
            if len(frames) < frame_count:
                frames.append(page)
                reference_bits.append(1)
            else:
                # Memory is full, we need to find a victim page
                # Move the pointer until we find a page with reference bit 0
                while reference_bits[pointer] == 1:
                    # Give it a second chance by setting its bit to 0
                    reference_bits[pointer] = 0
                    # Move pointer forward in circular order
                    pointer = (pointer + 1) % frame_count
                
                # Replace the victim page with the new page
                frames[pointer] = page
                # Set the new page's reference bit to 1
                reference_bits[pointer] = 1
                # Move pointer forward in circular order
                pointer = (pointer + 1) % frame_count

        # Save current step if trace is enabled
        if trace:
            trace_steps.append({
                "page": page, 
                "result": access_result, 
                "frames": frames.copy(), 
                "reference_bits": reference_bits.copy(), 
                "pointer": pointer
            })

    # Store final results after processing all pages
    result = {"faults": faults, "hits": hits, "final_frames": frames}
    
    # Attach trace if needed
    if trace: 
        result["trace"] = trace_steps
        
    return result