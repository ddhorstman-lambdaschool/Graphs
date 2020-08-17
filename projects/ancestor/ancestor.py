
def earliest_ancestor(ancestors, starting_node):

    parents_list = {}
    for parent, child in ancestors:
        if child not in parents_list:
            parents_list[child] = set()
        parents_list[child].add(parent)

    lineages = []

    def climb_lineage(lineage):
        current_ancestor = lineage[-1]

        # Reached the end of the lineage - add it to the list
        if current_ancestor not in parents_list:
            lineages.append(lineage)

        # Still more parents - follow their lineage
        else:
            for parent in parents_list[current_ancestor]:
                climb_lineage([*lineage, parent])

    climb_lineage([starting_node])

    # Trivial case - only one lineage (zero isn't possible)
    if len(lineages) == 1:
        ancestor = lineages[0][-1]
        return ancestor if ancestor != starting_node else -1

    # Multiple lineages
    lineages = sorted(lineages, key=len)
    longest_lineage = lineages.pop()
    oldest_ancestor = longest_lineage[-1]

    while len(lineages) > 0:
        next_longest_lineage = lineages.pop()

        # If this lineage is shorter than the last one, we're done
        if len(next_longest_lineage) < len(longest_lineage):
            return oldest_ancestor

        # If lengths are tied, the oldest ancestor
        # is the one with the smallest ID
        elif next_longest_lineage[-1] < oldest_ancestor:
            oldest_ancestor = next_longest_lineage[-1]

    return oldest_ancestor
