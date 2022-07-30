# Name: Aaron Wheaton

# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out


    def empty_buckets(self) -> int:
        """
        This method returns how many empty buckets are in the hash table
        """
        len = self.buckets.length()
        empty_count = 0
        # Gets the length of the hash map, and goes down each line. 
        # If it sees no head (basically no nodes), then it adds one to the empty rows counter, 
        # and moves to the next. Lastly, returns the count of empty rows.
        for i in range(0, len):
            if self.buckets.get_at_index(i).head is None:
                empty_count += 1
        
        return empty_count

    def table_load(self) -> float:
        """
        This method returns the hash table load factor.
        """
        len = self.buckets.length()
        total_count = 0
        bucket_count = 0
        # Goes row by row, adds each linked list item to total count, and 1 for each bucket row.
        # Then performs the calculation in the explorations, and returns the value.
        for i in range(0, len):
            total_count += self.buckets.get_at_index(i).length()
            bucket_count += 1

        load_factor = total_count / bucket_count

        return load_factor


    def put(self, key: str, value: object) -> None:
        """
        TODO: This method updates the key/value pair in the hash map.
        """
        # Calculate index using hash function and modulo operator.
        bucket_hash = self.hash_function(key)
        bucket_location = bucket_hash % self.capacity
        # Pull the "hash row" and assign that to object "bucket"
        bucket = self.buckets.get_at_index(bucket_location)
        bucket_check = bucket.contains(key)
        # If key isnt located, insert
        if bucket_check is None:
            bucket.insert(key, value)
            self.size += 1
        # If key is located, remove prior node, and replace with new node.
        else:
            bucket.remove(key)
            bucket.insert(key, value)
        

    def get(self, key: str) -> object:
        """
        This method returns a value associated with a given key.
        """
        # Almost identical to put code, only now we're returning the value if the key is found
        bucket_hash = self.hash_function(key)
        bucket_location = bucket_hash % self.capacity
        bucket = self.buckets.get_at_index(bucket_location)
        bucket_check = bucket.contains(key)
        if bucket_check is None:
            return None
        else:
            return bucket_check.value

    def clear(self) -> None:
        """
        This method clears the contents of the hash table without modifying the hash table
        capacity 
        """
        # Basically replaces every row of the hash table with an empty LL, and sets the size to 0.
        len = self.buckets.length()
        for i in range(0, len):
            self.buckets.set_at_index(i, LinkedList())

        self.size = 0

    def remove(self, key: str) -> None:
        """
        This method allows a user to remove a key and its associated value from the hash table.
        """
        # Identical "search by key" code to put, only now it utilizes the remove LL method, and reduces
        # the size by 1.
        bucket_hash = self.hash_function(key)
        bucket_location = bucket_hash % self.capacity
        bucket = self.buckets.get_at_index(bucket_location)
        bucket_check = bucket.contains(key)
        if bucket_check is None:
            return 
        else:
            bucket.remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        This method checks if a key exists in the hash table. Returns True if exists, False if doesnt.
        """
        # Again, identical search by key code from put, only now we return a bool depending
        # on conditional results.
        bucket_hash = self.hash_function(key)
        bucket_location = bucket_hash % self.capacity
        bucket = self.buckets.get_at_index(bucket_location)
        bucket_check = bucket.contains(key)
        if bucket_check is None:
            return False
        else:
            return True


    def resize_table(self, new_capacity: int) -> None:
        """
        This method resizes the hash table while preserving all the hashes.
        """
        # Edge case for capacity less than one
        if new_capacity < 1:
            return 
        # Creates a "storage bucket" DA, which holds all the rows of the current DA
        storage_bucket = DynamicArray()
        da_len = self.buckets.length()
        for i in range(0, da_len):
            row = self.buckets.get_at_index(i)
            storage_bucket.append(row)
        # Empties the old bucket, changes capacity, and sets size to 0 since there are now
        # no values  in the current bucket
        self.buckets = DynamicArray()
        self.capacity = new_capacity
        self.size = 0
        # Adds all empty linked lists for the new capacity
        for _ in range(new_capacity):
            self.buckets.append(LinkedList())
        da_len = storage_bucket.length()
        # Any values in the storage DA are appended to the main DA
        for i in range(0, da_len):
            bucket = storage_bucket.get_at_index(i)
            bucket_len = bucket.length()
            if bucket_len > 0:
                for node in bucket:
                    self.put(node.key, node.value)


    def get_keys(self) -> DynamicArray:
        """
        This method returns a DA that contains all keys in hashmap
        """
        key_da = DynamicArray()
        table_len = self.buckets.length()
        # Iterates through the hash map, and if any keys are found, appends them to the key da,
        # which is then returned.
        for i in range(0, table_len):
            bucket = self.buckets.get_at_index(i)
            bucket_len = bucket.length()
            if bucket_len > 0:
                for node in bucket:
                    key_da.append(node.key)

        return key_da


# BASIC TESTING
# if __name__ == "__main__":

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)


    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)


    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())


    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)


    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)


    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))


    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)


    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))


    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')


    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(10, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         result &= m.contains_key(str(key))
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())

    # m.resize_table(1)
    # print(m.get_keys())

    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
