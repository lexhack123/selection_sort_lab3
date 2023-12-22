import mysql.connector, random, time, sys, os

# Get the current directory main.py
current_dir = os.path.dirname(__file__)




PythonApplication1_path = os.path.abspath(os.path.join(current_dir, '..', 'PythonApplication1'))
sys.path.append(PythonApplication1_path)


from selection_sort import selection_sort2



def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='work123',
        database='array_storage'
    )


def add_arrays(num_arrays):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        start_time = time.time()

        for _ in range(num_arrays):
            # Generate a random array
            array = [random.randint(1, 100) for _ in range(random.randint(5, 15))]
            # Insert the array into the database
            cursor.execute('INSERT INTO unsorted_arrays (unsorted_array_data) VALUES (%s)', (str(array),))

        conn.commit()
        conn.close()

        execution_time = time.time() - start_time
        print(f'Added {num_arrays} arrays in {execution_time} seconds.')

    except mysql.connector.Error as error:
        print(f'Error adding arrays: {error}')

def fetch_and_sort_arrays(num_arrays):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Retrieve data from the unsorted_arrays table
        cursor.execute(f'SELECT unsorted_array_data FROM unsorted_arrays ORDER BY RAND() LIMIT {num_arrays}')
        arrays = cursor.fetchall()

        start_time = time.time()

        sorted_arrays = []  # Create an empty list for sorted arrays

        for array in arrays:
            # Sort each array and append it to the list of sorted arrays
            sorted_array = selection_sort2(eval(array[0]))
            sorted_arrays.append(sorted_array)

        # Write sorted data to the sorted_arrays table
        for sorted_array in sorted_arrays:
            cursor.execute('INSERT INTO sorted_arrays (sorted_array_data) VALUES (%s)', (str(sorted_array),))

        conn.commit()

        execution_time = time.time() - start_time
        avg_sorting_time = execution_time / len(arrays)

        print(
            f'Fetched {num_arrays} arrays from unsorted_arrays, sorted, and written to sorted_arrays in {execution_time} seconds.')
        print(
            f'Average sorting time for 1 array: {avg_sorting_time} seconds.')

    except mysql.connector.Error as error:
        print(f'Error fetching and sorting arrays: {error}')

def clear_database():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        start_time = time.time()
        cursor.execute('DELETE FROM unsorted_arrays')
        cursor.execute('DELETE FROM sorted_arrays')
        conn.commit()
        conn.close()

        execution_time = time.time() - start_time
        print(f'Database cleared in {execution_time} seconds.')

    except mysql.connector.Error as error:
        print(f'Error clearing the database: {error}')

# Run tests
add_arrays(100)  # Add 100 arrays to the database
add_arrays(1000)  # Add 1000 arrays to the database
add_arrays(10000)  # Add 10000 arrays to the database

# Fetch and sort 100, 1000, and 10000 random arrays from the database
fetch_and_sort_arrays(100)
fetch_and_sort_arrays(1000)
fetch_and_sort_arrays(10000)

# Clear the database
clear_database()

