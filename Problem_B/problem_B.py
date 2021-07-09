import sys
from copy import deepcopy


# Description: If the parent isn't in the tree it is inserted with 0 royal blood,
# 		no parents and with only this child in the list of children. If it exists
# 		then the child is appended to the list of children.
# Receives: Genealogy tree, the names of one parent and the name of a child.
# Returns: The genealogy tree with one parent inserted/modified in it.
def update_parent(royal_family, parent, child):
	if parent in royal_family:
		royal_family[parent][2].append(child)
	else:
		royal_family[parent] = [0.0, (None, None), [child]]
	return royal_family


# Description: The functions inserts/modifies the parents' information.
# Receives: Genealogy tree, the names of the parents and the name of the child.
# Returns: The genealogy tree with the parents inserted/modified in it.
def update_parents(royal_family, parent1, parent2, child):
	royal_family = update_parent(royal_family, parent1, child)
	royal_family = update_parent(royal_family, parent2, child)
	return royal_family


# Description: The functions calculates the royal blood of a child based on its parents.
# Receives: Genealogy tree, the names of two parents.
# Returns: The average royal blood of the child.
def get_bloodline_value(royal_family, parent1, parent2):
	bloodline1 = royal_family[parent1][0]
	bloodline2 = royal_family[parent2][0]
	return float(bloodline1 + bloodline2)/2.0


# Description: This function introduces a child to the genealogy tree. It inserts
# 		a new instance with the parent's royal blood average and an empty list of children.
# Receives: Genealogy tree, the name of the child and the names of the parents.
# Returns: The genealogy tree updated with the child inserted in it.
def add_child_to_royal_family(royal_family, child, parent1, parent2):
	bloodline = get_bloodline_value(royal_family, parent1, parent2)
	royal_family[child] = [bloodline, (parent1, parent2), []]
	return royal_family 


# Description: The function updates the royal blood and the name of the child's parents.
# Receives: Genealogy tree, the names of the parents and the name of the child.
# Returns: The genealogy tree with the royal blood and the tuple of parents of the child updated. 
def update_child(royal_family, parent1, parent2, child):
	royal_family[child][0] = get_bloodline_value(royal_family, parent1, parent2)
	royal_family[child][1] = (parent1, parent2)
	return royal_family


# Description: The functions updates all the children's royal blood value that have
# 		been affected by the indroduction of a tuple of parents.
# Receives: Genealogy tree and the name of a child.
# Returns: The genealogy tree from the children's nodes downwards is
#		updated with the new royal blood value.
def update_children(royal_family, children):
	if len(children):
		child = children.pop()
		(parent1, parent2) = royal_family[child][1]
		bloodline = get_bloodline_value(royal_family, parent1, parent2)
		royal_family[child][0] = bloodline
		children = deepcopy(royal_family[child][2])
		update_children(royal_family, children)
	return royal_family


# Description: The functions updates the child by adding the parents,
# 		the royal blood and also updates all the other children of the parents.
# Receives: Genealogy tree, the names of the parents and the name of the child.
# Returns: The genealogy tree with the information of all children updated. 
def update_child_and_children(royal_family, parent1, parent2, child):
	royal_family = update_child(royal_family, parent1, parent2, child)
	children = deepcopy(royal_family[child][2])
	royal_family = update_children(royal_family, children)
	return royal_family


# Description: This function checks if the name of the person claiming the throne
# 		has a higher value of royal blood. If there has not been a claimer yet,
# 		it is automatically but temporarily awarded the throne.
# Receives: Genealogy tree, a claimer to the throne, the maximum of royal blood
# 			seen until now and the current candiate to be the king.
# Returns: The updated name of the new king to be and its royal blood value.
def check_claim(royal_family, claimer, max_royal_blood, new_king):
	try:
		if royal_family[claimer][0] > max_royal_blood:
			max_royal_blood = royal_family[claimer][0]
			new_king = claimer
	except KeyError:
		if max_royal_blood == -1:
			new_king = claimer
	return max_royal_blood, new_king


# 2 <= N, M <= 50
N, M = sys.stdin.readline().split()
king = sys.stdin.readline().rstrip()


# Genealogy tree. For every member contains the name as key,
# its royal blood, name of the parents and a list of the children.
royal_family = {king: [1.0, (None, None), []]}


for row in range(int(N)):
	# len(child, parent1, parent2) ~ [1..10], letters (a-z)
	child, parent1, parent2 = sys.stdin.readline().split()
	royal_family = update_parents(royal_family, parent1, parent2, child)
	if child in royal_family:
		# Here we have member of the royal family that until now it had no known parents.
		royal_family = update_child_and_children(royal_family, parent1, parent2, child)
	else:	
		royal_family = add_child_to_royal_family(royal_family, child, parent1, parent2)


max_royal_blood = 0.0
new_king = ''
for row in range(int(M)):
	claimer = sys.stdin.readline().rstrip()
	max_royal_blood, new_king = check_claim(royal_family, claimer, max_royal_blood, new_king)


print(new_king)

