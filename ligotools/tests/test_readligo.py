from ligotools import readligo as rl
import pytest 


def test_loaddata():
	assert len(rl.loaddata('data/H-H1_LOSC_4_V2-1126259446-32.hdf5', 'H1')) == 3
	
def test_FileList():
	file = rl.FileList()
	assert file.directory == '.'


def test_read_hdf5():
	import numpy as np
	assert isinstance(rl.read_hdf5('data/H-H1_LOSC_4_V2-1126259446-32.hdf5')[0], np.ndarray)

def test_dq2segs():
	assert str(rl.dq2segs(rl.loaddata('data/H-H1_LOSC_4_V2-1126259446-32.hdf5')[2], 0)) == 'SegmentList( [(0, 32)] )'
		
	