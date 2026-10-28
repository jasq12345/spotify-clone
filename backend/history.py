
    def delete_duplicate(self):
        seen = set()
        current = self.head

        while current is not None:
            next_node = current.next
            if current.song.id in seen:
                self.remove(current)
            else:
                seen.add(current.song.id)

            current = next_node
