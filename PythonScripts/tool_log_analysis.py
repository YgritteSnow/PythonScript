
def logAnalysis( origin_string ):
	filename = r"F:\MyProjects\DxDemo_1\DxDemo_1",
	
	filestr = open( filename , 'r+' )
	try:
		f_lines = filestr.readlines( 1000 )
		for line in f_lines:
			left_idx = line.find('use')
			right_idx_lock = line.find('lock')
			right_idx_unlock = line.find('unlock')