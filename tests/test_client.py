import threading
import time

from compas_rrc.client import SequenceCounter


def test_sequence_id_rollover():
    counter = SequenceCounter()
    assert counter.value == 0

    for i in range(1, 1000000):
        counter.increment()
        assert counter.value == i
    assert counter.value == 999999

    counter.increment()
    assert counter.value == 1000000

    counter.increment()
    assert counter.value == 1


def test_sequence_id_increments():
    counter = SequenceCounter()
    assert counter.value == 0
    counter.increment()
    assert counter.value == 1


def test_multithreaded_consistency():
    nr_of_threads = 4
    nr_of_increments = 1000
    counter = SequenceCounter()

    def incrementer(c):
        for i in range(nr_of_increments):
            c.increment()
            time.sleep(0.001)

    threads = []
    for _ in range(nr_of_threads):
        t = threading.Thread(target=incrementer, args=(counter, ))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    assert counter.value == nr_of_threads * nr_of_increments
