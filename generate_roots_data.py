from itertools import repeat
from time import perf_counter as time
import multiprocessing as mp
from quat_poly import quat_poly
from polynomial_generators import *

########## Choose Polynomials and Output Files ###############################

# my machine: 2 takes a few seconds, 3 takes a few minutes, 4 takes a few hours
degree = 4

polynomial_generator = all_signs_qp(degree)

individuals_file_path = f"degree_{degree}_individual_roots.csv"
classes_file_path = f"degree_{degree}_class_roots.csv"


########## Multiprocessing Stuff #############################################

def worker(coefs_q):
    """
    Finds the roots of the monic quaternion polynomial with the given
    non-leading coefficients, and adds its roots to the back of the given
    queue.

    :param coefs_q: A 2-tuple of:
        1. a list of coefficients, and
        2. The output queue to add the results to.
    """
    coefs, q = coefs_q
    q.put(quat_poly(*coefs, 1).distinct_roots())


def output_stream(q):
    """
    This is the sole process allowed to write to the output files. It uses
    a queue to ensure thread safety. Only called once. Stops execution once the
    string 'kill' appears at the front of the queue.

    :param q: The queue to output.
    """
    individuals_file = open(individuals_file_path, 'w')
    classes_file = open(classes_file_path, 'w')

    # Loop until we get a command to kill
    while True:
        # Wait for the queue to be nonempty
        m = q.get()

        if m == 'kill':
            break

        # The workers put pairs of lists on the queue.
        individuals, classes = m

        individuals_file.write(''.join(f'{a},{b},{c},{d}\n' for (a, b, c, d) in individuals))
        classes_file.write(''.join(f'{z.real},{z.imag}\n' for z in classes))

        individuals_file.flush()
        classes_file.flush()

    individuals_file.close()
    classes_file.close()


def main():
    """
    Initializes the multiprocessing and calls a worker for each
    polynomial; finds roots of all polynomials in the chosen generator
    and outputs them to files.
    """

    # Multiprocessing apparatus
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count() + 2)

    # Initialize the output stream
    pool.apply_async(output_stream, (q,))

    # Call `worker()` for each polynomial. Throw away the blank result.
    for _ in pool.imap_unordered(worker, zip(polynomial_generator, repeat(q)), chunksize=1000):
        pass

    # Clean up! Halt all running processes.
    q.put('kill')
    pool.close()
    pool.join()


if __name__ == '__main__':
    start_time = time()
    main()
    print(f"Time elapsed: ", time() - start_time)
