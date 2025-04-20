from kalaha import config

from typing import Optional
from kalaha.models.game import Pit


class PitNode:
    def __init__(self, id: int, column: int, value: Pit):
        self.id = id
        self.column = column
        self.value: Pit = value
        self.count = self.value.count
        self.next: Optional[PitNode] = None

    def __repr__(self) -> str:
        return f"Node(id={self.id}, value={self.value})"


class PitsList:
    """
    Circular Linked List. Each node points to the next node, and the last node points back to the head.
    self._nodes_map stores a dictionary where key it is node ID and the value is the node instance.
    self._columns_map stores a dictionary where key it is column ID and the value is a tuple where
    the first element is a node of one player, and the second element is a node of another player.
    """

    def __init__(self, pits: list[Pit]):
        self.head: Optional[PitNode] = None
        self.last: Optional[PitNode] = None
        self._nodes_map = dict()
        self._columns_map: dict[int, list[PitNode | None]] = {
            column: [None, None] for column in range(config.PITS_PER_USER)
        }
        self._generate_list(pits)

    def _generate_list(self, pits: list[Pit]):
        for pit in pits:
            self._append(pit)

    def _append(self, value: Pit):
        node = PitNode(value.id, value.column, value)

        if self.head is None or self.last is None:
            self.head = node
            self.last = node
        else:
            self.last.next = node
            self.last = node

        self.last.next = self.head

        self._nodes_map[node.id] = node
        self._columns_map[node.column][value.player_id] = node

    def get_node_by_id(self, id: int) -> PitNode:
        node = self._nodes_map.get(id)
        if node is None:
            raise ValueError("Node cannot be found, Invalid ID")

        return node

    def get_opposite_node(self, node: PitNode) -> PitNode:
        opposite = self._columns_map.get(node.column)[
            int(not bool(node.value.player_id))
        ]
        return opposite


class PitsListIterator:
    def __init__(self, start_node: PitNode | None, max_steps: int):
        """
        Iterator required start_node instance that is used as a starting point.

        @param max_steps: max number of iterations.
        """
        self.current = start_node
        self.max_steps = max_steps
        self.iteration = 0

    def __iter__(self):
        return self

    def __next__(self) -> PitNode:
        if not self.current or self.iteration == self.max_steps:
            raise StopIteration
        node = self.current
        self.current = self.current.next
        self.iteration += 1
        return node
