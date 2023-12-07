class DFS:
    @staticmethod
    def topological_sort(graph: dict):
        visited = set()
        stack = []

        def dfs(node):
            print(len(graph[node]))
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


class SortByDetph:
    @staticmethod
    def sort(graph: dict):
        sorted_graph = SortByDetph._sort_dict_by_set_size(graph)
        res = []
        for key, value in sorted_graph:
            res.append(key)
        return res

    @staticmethod
    def _sort_dict_by_set_size(input_dict):
        depth_dict = SortByDetph._get_depth_dict(input_dict)
        sorted_items = sorted(depth_dict.items(), key=lambda x: x[1])
        return sorted_items

    @staticmethod
    def _get_depth_dict(input_dict):
        depth_dict = {}
        for key, value in input_dict.items():
            depth_dict[key] = SortByDetph._get_depth(input_dict, key)
        return depth_dict

    @staticmethod
    def _get_depth(input_dict, key):
        depth = 0
        for value in input_dict[key]:
            depth = max(depth, SortByDetph._get_depth(input_dict, value))
        return depth + 1
