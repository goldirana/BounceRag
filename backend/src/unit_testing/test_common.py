import unittest
from backend.src.utils.common import perform_multiprocessing
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def sample_function(x):
    return x * x

class TestPerformMultiprocessing(unittest.TestCase):
    def test_perform_multiprocessing(self):
        iterable = [1, 2, 3, 4, 5]
        expected_result = [x * x for x in iterable]
        
        with Pool(processes=cpu_count()) as pool:
            result = list(tqdm(pool.imap(sample_function, iterable), total=len(iterable)))
        
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()