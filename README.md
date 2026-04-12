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

Use of AI

- AI tools were used to help understand the algorithms and organize the explanation  
- The final code and explanation were reviewed and understood before submission  
