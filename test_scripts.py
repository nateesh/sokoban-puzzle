from sokoban import Warehouse
from mySokobanSolver import SokobanPuzzle, is_possible_move, find_steps


try:
    from fredSokobanSolver import solve_weighted_sokoban, check_elem_action_seq
    print("Using Fred's solver")
except ModuleNotFoundError:
    from mySokobanSolver import solve_weighted_sokoban, check_elem_action_seq
    print("Using submitted solver")

# Unit test for functions
def unit_test_is_possible_move():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_99.txt")
    # 1st test: correct move
    print('<<  unit_test_is_possible_move, test 1>>')
    action_seq = ['Right','Right']
    expected_answer = 'True'
    for action in action_seq:  
        # Check if the given action sequence is valid or not by calling is_possible_move()
        # If it's not valid move => return Impossible
        if is_possible_move(wh, action):
            answer = 'True'
        else:
            answer = 'False'
    if answer==expected_answer:
        print('Test 1 passed!  :-)\n')
    else:
        print('Test 1 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)


def test_check_elem_action_seq():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/customize/warehouse_8c.txt")
    # 1st test: correct move
    answer = check_elem_action_seq(wh, ['Up', 'Up','Left'])
    expected_answer = '#############\n#    @ # #  #\n#   $       #\n# *        .#\n#############'
    print(expected_answer)
    print('<<  check_elem_action_seq, test 1, correct move>>')
    if answer==expected_answer:
        print('Test 1 passed!  :-)\n')
    else:
        print('Test 1 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # 2nd test: inccorect move
    answer = check_elem_action_seq(wh, ['Down', 'Down','Right'])
    expected_answer = 'Impossible'
    print('<<  check_elem_action_seq, test 2, impossible move>>')
    if answer==expected_answer:
        print('Test 2 passed!  :-)\n')
    else:
        print('Test 2 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # 3rd test (Expected: Impossible): move to wall
    answer = check_elem_action_seq(wh, ['Up', 'Up','Right'])
    expected_answer = 'Impossible'
    print('<<  check_elem_action_seq, test 3, impossible move worker to wall>>')
    if answer==expected_answer:
        print('Test 3 passed!  :-)\n')
    else:
        print('Test 3 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # 4th test: correct move to empty cell between walls
    answer = check_elem_action_seq(wh, ['Up', 'Right', 'Right','Up'])
    expected_answer = '#############\n#      #@#  #\n#   $       #\n# *        .#\n#############'
    print('<<  check_elem_action_seq, test 4, correct move>>')
    if answer==expected_answer:
        print('Test 4 passed!  :-)\n')
    else:
        print('Test 4 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # 5th test: correct move worker push box
    answer = check_elem_action_seq(wh, ['Up', 'Left', 'Left','Left', 'Left'])
    expected_answer = '#############\n#      # #  #\n#$@         #\n# *        .#\n#############'
    print('<<  check_elem_action_seq, test 5, correct move>>')
    if answer==expected_answer:
        print('Test 5 passed!  :-)\n')
    else:
        print('Test 5 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # 6th test: impossible move worker push box to wall
    answer = check_elem_action_seq(wh, ['Up', 'Left', 'Left','Left', 'Left','Left'])
    expected_answer = 'Impossible'
    print('<<  check_elem_action_seq, test 6: impossile move box to wall>>')
    if answer==expected_answer:
        print('Test 6 passed!  :-)\n')
    else:
        print('Test 6 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    
def test_solve_weighted_sokoban():
    wh = Warehouse()    
    wh.load_warehouse( "./warehouses/customize/warehouse_09b.txt")
    # 1st test: Boxes already in targets
    answer, cost = solve_weighted_sokoban(wh)

    expected_answer = [] 
    expected_cost = 0
    print('<<  test_solve_weighted_sokoban, test 1, boxes already in target >>')
    if answer==expected_answer:
        print('Test 1 passed!  :-)\n')
    else:
        print('Test 1 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        print('Your answer is different but it might still be correct')
        print('Check that you pushed the right box onto the left target!')
    print(f'1st test: Your cost = {cost}, expected cost = {expected_cost}')

    # 2nd test: box with smaller weight already in target and stay in corner => cannot move
    wh.load_warehouse( "./warehouses/customize/warehouse_8d.txt")
    answer, cost = solve_weighted_sokoban(wh)

    expected_answer = ['Left', 'Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left'] 
    expected_cost = 207
    print('<<  test_solve_weighted_sokoban, test 2,  light weight box cannot move>>')
    if answer==expected_answer:
        print('Test 2 passed!  :-)\n')
    else:
        print('Test 2 failed!  :-(\n')
        print('Expected ');print(expected_answer)
    print(f'2nd test: Your cost = {cost}, expected cost = {expected_cost}')

    # 3rd test: Impossible warehouse with box in corners
    wh.load_warehouse( "./warehouses/customize/warehouse_8i.txt")
    answer, cost = solve_weighted_sokoban(wh)

    expected_answer = 'Impossible'
    expected_cost = None
    print('<<  test_solve_weighted_sokoban, test 3,  impossible move with box in corners>>')
    if answer==expected_answer:
        print('Test 3 passed!  :-)\n')
    else:
        print('Test 3 failed!  :-(\n')
        print('Expected ');print(expected_answer)
    print(f'3rd test: Your cost = {cost}, expected cost = {expected_cost}')

    # 4th test: testing light box (weight 1), and heavy box (weight 99)
    # Eventhough light box near a target (2 targets), but this box still has been move to
    # the target that was initially the farthest.

    wh.load_warehouse( "./warehouses/customize/warehouse_8e.txt")
    answer, cost = solve_weighted_sokoban(wh)

    expected_answer = ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 
    'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 
    'Down', 'Left', 'Left', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right']
    expected_cost = 430
    print('<<  test_solve_weighted_sokoban, test 4,  light box and heavy box move>>')
    if answer==expected_answer:
        print('Test 4 passed!  :-)\n')
    else:
        print('Test 4 failed!  :-(\n')
        print('Expected ');print(expected_answer)
    print(f'3rd test: Your cost = {cost}, expected cost = {expected_cost}')

if __name__ == "__main__":
    unit_test_is_possible_move()
    test_check_elem_action_seq()
    test_solve_weighted_sokoban()