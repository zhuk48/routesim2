PREREQUISITES:

$ pip install networkx matplotlib

TO RUN:

$ python sim.py GENERIC demo.topo demo.event

ON MURPHY:

$ scl enable rh-python35 bash
$ python3.5 -m venv --system-site-packages virtualenv
$ . virtualenv/bin/activate
$ pip install --user matplotlib networkx

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
     0. # [comment]
        e.g. # this is a comment

     1. [Time] ADD_NODE [ID], # [ID] is any hashable value
        e.g., 10 ADD_NODE 1
     2. [Time] ADD_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 10 ADD_LINK 1 2 10
     3. [Time] DELETE_NODE [ID], # [ID] is any hashable value
        e.g., 10 DELETE_NODE 1
     4. [Time] DELETE_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 10 DELETE_LINK 1 2 10
     5. [Time] CHANGE_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 10 CHANGE_LINK 1 2 10

     6. [Time] PRINT [Text]
        e.g. 10 PRINT "Debug information"
     7. [Time] DRAW_TOPOLOGY
        e.g. 10 DRAW_TOPOLOGY
     8. [Time] DRAW_PATH [ID] [ID]
        e.g. 1000 DRAW_PATH 1 2

     9. [Time] DUMP_TABLE [ID]
        e.g. 10 DUMP_TABLE 1

