
ROUTE_ALGORITHM = {
    "GENERIC" : 0,
    "DISTANCE_VECTOR" : 1,
    "LINK_STATE" : 2
}

class EVENT_TYPE:
    ADD_NODE = "ADD_NODE"
    ADD_LINK = "ADD_LINK"

    DELETE_NODE = "DELETE_NODE"
    DELETE_LINK = "DELETE_LINK"

    CHANGE_LINK = "CHANGE_LINK"

    PRINT = "PRINT"
    DRAW_TOPOLOGY = "DRAW_TOPOLOGY"
    DRAW_PATH = "DRAW_PATH"
    DUMP_TABLE = "DUMP_TABLE"


EVENT_PATH = "event/"

TOPO_PATH = "topo/"

USAGE_STR = "usage: sim.py route_algorithm topology event\n" \
            "\troute_algorithm\t- {GENERIC DISTANCE_VECTOR LINK_STATE}\n" \
            "\ttopology\t\t- a file\n" \
            "\tevent\t\t\t- a file"