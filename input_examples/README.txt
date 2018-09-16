# to run (replace trivial.txt with whichever .txt):

python3 convert.py < trivial.txt | python3 prove.py


# only converter part:

python3 convert.py < sentences.txt


# only resolution part:

python3 prove.py < ex1_cnf.txt

# all the test files from the professor are included
# 2 extra files: ex1_cnf.txt and ex2.txt, 2 problems from the classes solved correctly (logic_a.pdf, pages 56 and 57)
# ex1_cnf.txt is in CNF, so it can be fed directly to prove.py or go through convert.py anyway
