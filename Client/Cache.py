import shelve


class Cache:
    def __init__(self, filename):
        self.filename = filename
        self.cache = shelve.open(self.filename)

    def __enter__(self):
        return self.cache

    def __exit__(self, exc_type, exc_value, traceback):
        self.cache.close()

    def get(self, key):
        """'
        :argument key: key to get from cache [host-name/path]
        """
        return self.cache[key]

    def set(self, key, value):
        """'
        :argument key: key to set in cache [host-name/path]
        :argument value: value to set in cache
        """
        self.cache[key] = value

    def is_cached(self, key):
        """'
        :argument key: key to check if in cache [host-name/path]
        """
        return key in self.cache

    def clear(self):
        """'
        :return: clear cache
        """
        self.cache.clear()

    def close(self):
        """'
        :return: close cache
        """
        self.cache.close()

    def delete(self, key):
        """'
        :argument key: key to delete
        """
        del self.cache[key]
