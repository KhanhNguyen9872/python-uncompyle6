# Hard: linked list (simpler)
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def build_list(values):
    head = None
    for v in values:
        node = Node(v)
        node.next = head
        head = node
    return head

def to_list(head):
    result = []
    cur = head
    while cur:
        result.append(cur.val)
        cur = cur.next
    return result

h = build_list([1, 2, 3])
print(to_list(h))
