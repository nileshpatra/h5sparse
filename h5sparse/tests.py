import os
from tempfile import mkstemp

import scipy.sparse as ss
import h5sparse
import numpy as np


def test_create_and_read_dataset():
    h5_path = mkstemp(suffix=".h5")[1]
    sparse_matrix = ss.csr_matrix([[0, 1, 0],
                                   [0, 0, 1],
                                   [0, 0, 0],
                                   [1, 1, 0]],
                                  dtype=np.float64)
    with h5sparse.File(h5_path) as h5f:
        h5f.create_dataset("sparse/matrix", data=sparse_matrix)
    with h5sparse.File(h5_path) as h5f:
        assert (h5f['sparse']['matrix'][1:3] != sparse_matrix[1:3]).size == 0
        assert (h5f['sparse']['matrix'][2:] != sparse_matrix[2:]).size == 0
        assert (h5f['sparse']['matrix'][:2] != sparse_matrix[:2]).size == 0
        assert (h5f['sparse']['matrix'][-2:] != sparse_matrix[-2:]).size == 0
        assert (h5f['sparse']['matrix'][:-2] != sparse_matrix[:-2]).size == 0
        assert (h5f['sparse']['matrix'].value != sparse_matrix).size == 0

    os.remove(h5_path)
