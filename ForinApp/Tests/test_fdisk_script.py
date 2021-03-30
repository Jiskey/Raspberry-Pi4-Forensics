#fdisk_Script Test File

import pytest

from Scripts.FdiskScript import *

def test_fdisk():
	txt_lines = fdisk()
	assert len(txt_lines) > 0
