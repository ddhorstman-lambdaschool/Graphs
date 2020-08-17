"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if self.vertices.get(vertex_id) is None:
            self.vertices[vertex_id] = set()
        else:
            raise ValueError(f"Identifier {vertex_id} already in use")

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v2]  # Raise a KeyError if v2 isn't in the graph
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        # Will raise an error if given an invalid vertex ID
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        node_queue = Queue()
        visited = set()

        node_queue.enqueue(starting_vertex)

        while node_queue.size() > 0:
            current = node_queue.dequeue()
            if current in visited:
                continue
            print(current)
            visited.add(current)
            for node in self.get_neighbors(current):
                node_queue.enqueue(node)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        node_stack = Stack()
        visited = set()

        node_stack.push(starting_vertex)

        while node_stack.size() > 0:
            current = node_stack.pop()
            if current in visited:
                continue
            print(current)
            visited.add(current)
            for node in self.get_neighbors(current):
                node_stack.push(node)

    def dft_recursive(self, current, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # Avoid python default args bug elaborated on elsewhere.
        visited = visited or set()

        if current in visited:
            return

        visited.add(current)
        print(current)

        for node in self.get_neighbors(current):
            self.dft_recursive(node, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        visited = set()
        node_queue = Queue()
        node_queue.enqueue((starting_vertex, []))

        while node_queue.size() > 0:
            current, path = node_queue.dequeue()

            if current in visited:
                continue

            visited.add(current)

            if current == destination_vertex:
                return [*path, current]

            for node in self.get_neighbors(current):
                # It's important to pass a copy of the path
                # so it isn't modified by multiple items in the queue
                node_queue.enqueue((node, [*path, current]))
        
        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        visited = set()
        node_stack = Stack()
        node_stack.push((starting_vertex, []))

        while node_stack.size() > 0:
            current, path = node_stack.pop()

            if current in visited:
                continue

            visited.add(current)

            if current == destination_vertex:
                return [*path, current]

            for node in self.get_neighbors(current):
                # Enforce path immutability
                node_stack.push((node, [*path, current]))
        
        return None      

    def dfs_recursive(self, current, destination, path=None, visited=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if destination not in self.vertices:
            raise KeyError(destination)

        # Providing default values in the function definition doesn't work,
        # as the defaults will be mutated the first time the function is called.
        # Hence it's necessary to default them to None
        # and provide a new empty array or set as fallback inside the function body.
        path = path or []
        visited = visited or set()

        if current == destination:
            return [*path, current]

        elif current not in visited:
            visited.add(current)

            for neighbor in self.get_neighbors(current):
                result = self.dfs_recursive(
                    neighbor,
                    destination,
                    # 'Path' is copied rather than passed directly
                    # to prevent multiple function calls from modifying the same list
                    [*path, current],
                    visited,
                )
                if result is not None:
                    return result
        else:
            return None


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
