Different from minet lab:
- Graph is undirected graph
    - Thus: we do not need to add link (2, 1) after add link (1, 2)
- Remove useless parameters
    1. Remove "bandwidth" and "latency" from a node
        - 0 ADD_NODE 1 1 1 -> 0 ADD_NODE 1
    2. Remove "bandwidth" from a link
        - 0 ADD_LINK 1 2 10 10 -> 0 ADD_LINK 1 2 10

- Remove useless function
    1. Remove "SendToNeighbor" function, only "SendToNeighbors" is useful.


topo command:
    0. # [comment]
        e.g. # this is a comment
    1. [Time] ADD_NODE [ID], # [ID] is any hashable value
        e.g., 0 ADD_NODE 1
    2. [Time] ADD_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 0 ADD_LINK 1 2 10

event command:


Question:
- In order to implement "GetNeighbors" and "SendToNeighbors" function, we have to send simulator point to Node
- How could forbid student to call other function in simulator?
- I think "GetNeighbors" function is not necessary, however, "SendToNeighbors" must use simulator point