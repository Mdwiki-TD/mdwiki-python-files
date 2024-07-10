# find      :   \s*\n(\s*#\s*[-]+\s*)+\n*^def
# find      :   \s*\n(#\s*[-]+\s*)+\n*def
# replace   :   \n\n\ndef


# find      :   \s*\n(\s*#\s*[-]+\s*)+\n*^(\s*def )
# replace   :   \n\n\n$2
