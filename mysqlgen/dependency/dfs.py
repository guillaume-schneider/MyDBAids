class DFS:
    @staticmethod
    def topological_sort(graph: dict):
        visited = set()
        stack = []

        def dfs(node):
            nonlocal visited
            visited.add(node)
            if node in graph:
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        dfs(neighbor)
            stack.append(node)

        for node in graph:
            if node not in visited:
                dfs(node)

        return stack[::-1]

