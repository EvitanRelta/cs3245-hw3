from typing import Iterable, Iterator


class LinkedList(Iterable):
    """Linked-list implementation to contain integer values."""

    NULL_NODE: "LinkedList" = None  # type: ignore
    """The linked-list node that represents the lack of any values."""

    def __init__(self, value: int) -> None:
        """
        Args:
            value (int): Value in the skip-list node.
        """
        self.value: int = value
        self.next_node = LinkedList.NULL_NODE

    def is_null_node(self) -> bool:
        return self is LinkedList.NULL_NODE

    def __len__(self) -> int:
        for i, _ in enumerate(self, start=1):
            pass
        return i

    def __iter__(self) -> Iterator[int]:
        node = self
        while not node.is_null_node():
            yield node.value
            node = node.next_node

    def deep_copy(self) -> "LinkedList":
        """Recursively copies all the `LinkedList` nodes."""
        iterator = iter(self)
        first_node = LinkedList(next(iterator))
        current_node = first_node
        for value in iterator:
            current_node.next_node = LinkedList(value)
            current_node = current_node.next_node
        return first_node

    @staticmethod
    def from_list(lst: list[int]) -> "LinkedList":
        """Converts a list into a `LinkedList`"""
        output = LinkedList.NULL_NODE
        last_node = LinkedList.NULL_NODE  # type: ignore

        for i, v in enumerate(lst):
            # First node.
            if i == 0:
                output = LinkedList(v)
                last_node = output
                continue

            last_node.next_node = LinkedList(v)
            last_node = last_node.next_node

        return output

    def __repr__(self) -> str:
        if self.is_null_node():
            return "NULL"

        node = self
        output = ""
        while not node.is_null_node():
            output += f"{node.value} -> "
            node = node.next_node

        return output + "NULL"


LinkedList.NULL_NODE = LinkedList(None)  # type: ignore
LinkedList.NULL_NODE.next_node = LinkedList.NULL_NODE
