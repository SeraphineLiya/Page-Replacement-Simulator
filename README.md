FIFO and LRU Page Replacement

FIFO (First In First Out)

- FIFO removes the page that has been in memory the longest  
- Pages are replaced in the same order they were added  
- A list called frames is used to store the current pages in memory  
- A variable called replace_index keeps track of which page should be replaced next  
- When a page fault happens, and memory is full:
  - the page at replace_index is replaced  
  - replace_index moves forward in a circular order using  
    replace_index = (replace_index + 1) % frame_count  
- This continues until all page references are processed  
- FIFO is simple, but does not consider how recently a page was used  

LRU (Least Recently Used)

- LRU removes the page that has not been used for the longest time  
- It focuses on how recently a page was accessed, not when it entered memory  
- A list called frames stores the current pages  
- A dictionary called last_used stores the last time each page was accessed  
- Each page is assigned a time based on its position in the reference sequence  
- When a page fault happens, and memory is full:
  - the page with the smallest last used time is selected  
  - that page is replaced with the new page  
- If two pages have the same priority, the smaller page number is chosen  
- LRU keeps recently used pages in memory, so it usually performs better than FIFO  

The Clock Algorithm keeps track of:
 - frames: the pages currently in memory
 - reference_bits: a bit for each page that shows if it was used recently
 - pointer: a circular pointer that moves through the frames like a clock hand

 When a page is accessed:
 - if the page is already in memory, it is a HIT
 - its reference bit is set to 1

 - if the page is not in memory, it is a FAULT
 - if there is space in memory, the page is added
 - if memory is full, the algorithm checks pages using the pointer

 When memory is full:
 - if a page has reference bit 1, it gets a second chance
 - its bit is changed to 0, and the pointer moves forward
 - this continues until a page with reference bit 0 is found
 - that page is replaced with the new page

 At the end, the function returns:
 - total page faults
 - total page hits
 - final frame contents
 - and, if trace=True, the step-by-step process

Integration and Routing
- this section acts as the central routing mechanism
- it connects the parsed JSON input to the specific page replacement algorithms
- a highly modular approach keeps the routing logic completely separate from the core algorithms

A function called run_simulation safely extracts parameters from the input dictionary:
- algorithm: the chosen replacement method
- frames: the number of memory frames
- references: the list of page numbers
- trace: optional parameter for step-by-step details

- it uses conditional routing to direct the execution flow to the appropriate function (FIFO, LRU, or Clock)
- it restructures the returned metrics into the strict JSON output format required by the assignment


Use of AI

- AI tools were used to help understand the algorithms and organize the explanation  
- The final code and explanation were reviewed and understood before submission  
