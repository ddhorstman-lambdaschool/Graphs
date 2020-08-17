from random import randint
from statistics import mean


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            raise ValueError("You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            raise ValueError("Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")
        # Create friendships
        remaining_friendships = num_users * avg_friendships // 2
        while remaining_friendships > 0:
            x = randint(1, num_users)
            y = randint(1, num_users)
            try:
                self.add_friendship(x, y)
                remaining_friendships -= 1
            except ValueError:
                continue

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        queue = [[user_id]]
        while len(queue) > 0:
            path = queue.pop(0)
            current_user = path[-1]
            if current_user not in visited:
                visited[current_user] = path
                for friend in self.friendships[current_user]:
                    queue.append([*path, friend])
        return visited


if __name__ == '__main__':
    percentages = []
    path_lengths = []
    sg = SocialGraph()
    for _ in range(1000):
        sg.populate_graph(1000, 5)
        # print(sg.friendships)
        connections = sg.get_all_social_paths(1)
        percentages.append(len(connections)/1000)
        path_lengths.append(mean([len(x) for x in connections.values()]))
    print(f"Percentage: {mean(percentages)*100:.1f}%")
    print(f"Degrees of Separation: {mean(path_lengths):.1f}")
