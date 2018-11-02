### PREREQUISITES:

    $ pip install networkx matplotlib

### TO RUN:

    $ python sim.py GENERIC demo.topo demo.event

### ON MURPHY:

    $ scl enable rh-python35 bash
    $ python3.5 -m venv --system-site-packages virtualenv
    $ . virtualenv/bin/activate
    $ pip install --user matplotlib networkx

### Different from minet lab:
- Graph is undirected graph
    - Thus: we do not need to add link (2, 1) after add link (1, 2)
- Remove useless parameters
    1. Remove "bandwidth" and "latency" from a node
        - 0 ADD_NODE 1 1 1 -> 0 ADD_NODE 1 // as well as DELETE_NODE
    2. Remove "bandwidth" from a link
        - 0 ADD_LINK 1 2 10 10 -> 0 ADD_LINK 1 2 10  // as well as CHANGE_LINK. DELETE_LINK only has two parameters.
- Remove some not interested commands
    1. DRAW_TREE [ID] . Since I think after implementing DRAW_PATH, we can see if it is easy to implemented in 
    
- Remove useless function
    1. ~~Remove "SendToNeighbor" function, only "SendToNeighbors" is useful.~~
    1.1. I add "send to neighbor" function back. We can use it to confuse students. ( •̀ ω •́ )y
    2. Remove "GetNeighbors" function. Node can only know their neighbors by "link_has_been_updated"
### Functions provide in Node class
    0. send_to_neighbors(m)  // send message to neighbors
    1. send_to_neighbor(neighbor, m) // send message to a neighbor
    2. get_time()  // get current simulator time (I think maybe useful in Link_State, since I use it last year.)
    

### Question
- If message arrive time = message send time + latency, a problem comes
    - suppose latency A to B is 100, A send message 1 at time 0, and will arrive at time 100
    - however, a link change is called at time 10, latency updated to 20
    - A send message 2 at time 20
    - message 2 should arrive at time 40
    - Then, how about message 1? arrive at 100 or at 40, or at 30?
    - In minet, it set to 100

### step options:
    0. NORMAL
        only stop when a picture is 
    1. SINGLE_STEP
        stop after an event
    2. NO_STOP
        no stop at all

### topo command:
    0. # [comment]
        e.g. # this is a comment
    1. [Time] ADD_NODE [ID], # [ID] is any hashable value
        e.g., 0 ADD_NODE 1
    2. [Time] ADD_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 0 ADD_LINK 1 2 10

### event command:
     0. # [comment]
        e.g. # this is a comment

     1. [Time] ADD_NODE [ID], # [ID] is any hashable value
        e.g., 10 ADD_NODE 1
     2. [Time] ADD_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 10 ADD_LINK 1 2 10
     3. [Time] DELETE_NODE [ID], # [ID] is any hashable value
        e.g., 10 DELETE_NODE 1
     4. [Time] DELETE_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 10 DELETE_LINK 1 2
     5. [Time] CHANGE_LINK [ID1] [ID2], # will send latency -1 to node1 and node 2
        e.g., 10 CHANGE_LINK 1 2 10

     6. [Time] PRINT [Text]
        e.g. 10 PRINT "Debug information"
     7. [Time] DRAW_TOPOLOGY
        e.g. 10 DRAW_TOPOLOGY
     8. [Time] DRAW_PATH [ID] [ID]
        e.g. 1000 DRAW_PATH 1 2

     9. [Time] DUMP_TABLE [ID]
        e.g. 10 DUMP_TABLE 1
     10. [Time] DUMP_SIM
        e.g. 1 DUMP_SIM # It will print topology and event stack. For debug purpose.

