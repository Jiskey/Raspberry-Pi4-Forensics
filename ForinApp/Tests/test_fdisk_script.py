#fdisk_Script Test File

import pytest
import os
import sys

from Scripts.FdiskScript import *

def test_fdisk():
	txt_lines = fdisk()
	assert len(txt_lines) > 0
	assert os.path.isfile('Config/fdisk_search.txt') == False
