from generic_node import Generic_Node
from distance_vector_node import Distance_Vector_Node
from link_state_node import Link_State_Node

ROUTE_ALGORITHM = [
    "GENERIC",
    "DISTANCE_VECTOR",
    "LINK_STATE"
]

ROUTE_ALGORITHM_NODE = {
    "GENERIC" : Generic_Node,
    "DISTANCE_VECTOR" : Distance_Vector_Node,
    "LINK_STATE" : Link_State_Node
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

LOGGING_FORMAT = "[%(asctime)s][%(levelname)s] %(name)s: %(message)s"

LOGGING_DATAFMT = '%Y-%m-%d %H:%M:%S'