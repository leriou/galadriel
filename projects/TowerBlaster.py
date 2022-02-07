from dis import dis
import random
from sklearn import tree
from sklearn import ensemble
from sklearn.neural_network import MLPClassifier
from sklearn import linear_model
from sklearn import svm
from sklearn.naive_bayes import GaussianNB

def ml_predict_discard(tower, discard_top):
    count_map = ml_get_result(tower, discard_top)
    if max(count_map.values()) >= 3:
        return random.randint(0, 1000) < 700
    else:
        return random.randint(0, 1000) < 500

def ml_get_result(tower, new_brick):
    t = tower[:] 
    t.append(new_brick)
    def read_train_data(file_name):
        x = []
        y = []
        with open(file_name, "r+") as f:
            for i in f.readlines():
                ns =i.split(",")
                x.append([int(p) for p in ns[:11]])
                y.append(int(ns[len(ns)-1].strip()))
            f.close()
        return (x,y)
    (x,y) = read_train_data("./record.csv")
    def get_predict_result(x, y):
        model_list = [
            tree.DecisionTreeClassifier(),
            ensemble.RandomForestClassifier(random_state=1),
            MLPClassifier(random_state=1,max_iter=400),
            linear_model.BayesianRidge(),
            svm.SVC(),
            GaussianNB()
        ]
        count_map = {}
        idx = 0
        for model in model_list:
            model.fit(x,y)
            predict_result = model.predict([t])
            idx+=1
            ans = round(predict_result[0])
            # print("【debug】 %s predict %s" %  ( idx, ans))
            if ans in count_map:
                count_map[ans] += 1
            else:
                count_map[ans] = 1
        return count_map
    return get_predict_result(x,y)

def mk_predict_replaced(tower, new_brick):
    count_map = ml_get_result(tower, new_brick)
    # print("【debug】%s " % count_map)
    for i in count_map:
        if count_map[i] == max(count_map.values()):
            return i

def train_log(tower, brick, brick_replaced):
    train_file = "./record.csv"
    t = tower[:]
    t.append(brick)
    t.append(brick_replaced)
    log = ",".join([str(i) for i in t]) + "\n"
    with open(train_file,"a+") as f:
        f.write(log)
        f.close()

def setup_bricks():
    main_piles,discard_piles = [i for i in range(1,1+60)],[]
    return (main_piles,discard_piles)

def shuffle_bricks(bricks):
    random.shuffle(bricks)

def check_bricks(main_pile, discard_pile):
    if len(main_pile) == 0:
        random.shuffle(discard_pile)
        main_pile,discard_pile = discard_pile,main_pile
        add_brick_to_discard(get_top_brick(main_pile), discard_pile)

def check_tower_blaster(tower):
    for i in range(0, len(tower)-1):
        if tower[i] > tower[i+1]:
            return False
    return True

def get_top_brick(brick_pile):
    brick_num = brick_pile[0]
    brick_pile.remove(brick_num)
    return brick_num

def deal_initial_bricks(main_pile):
    computer_tower, human_tower = [],[]
    for i in range(0,10):
        computer_tower.insert(0,get_top_brick(main_pile))
        human_tower.insert(0,get_top_brick(main_pile))
    return (computer_tower, human_tower)

def add_brick_to_discard(brick, discard_pile):
    discard_pile.insert(0,brick)

def find_and_replace(new_brick, brick_to_be_replaced, tower, discard_pile):
    if brick_to_be_replaced in tower:
        old_idx = tower.index(brick_to_be_replaced)
        tower[old_idx] = new_brick
        add_brick_to_discard(brick_to_be_replaced, discard_pile)
        return True
    return False

def computer_play(tower, main_pile, discard_pile):
    """
    computer's turn
    """
    print("COMPUTER'S TURN")
    (target_pile, brick_from) = choose_pile(tower, discard_pile, main_pile)

    brick = get_top_brick(target_pile)
    replaced_index = mk_predict_replaced(tower, brick)  
    replace_brick = tower[replaced_index]
    print("【debug】computer's tower %s will use %s replaced %s" % (tower, brick, replace_brick))
    if find_and_replace(brick, replace_brick, tower, discard_pile):
        print("The computer picked %s from %s pile" % (brick, brick_from))
    return tower

def choose_pile(tower, discard_pile, main_pile):
    """
    retrun  pile, discription
    """
    if len(discard_pile) > 1 and ml_predict_discard(tower, discard_pile[0]):
        return (discard_pile, "discard")
    else:
        return (main_pile, "main")


def human_play(tower, main_pile, discard_pile):
    print("NOW IT'S YOUR TURN")
    print("Your Tower: %s" % tower)
    print("The Top Brick in the discard pile is %s" % discard_pile[0])

    target_pile = []
    is_choosen_pile = False 
    while not is_choosen_pile:
        path_choose = input("Type 'D' to take the discard brick, 'M' for a mystery brick, or 'H' for help\n")
        if path_choose in ('D','d'):
            is_choosen_pile = True
            target_pile = discard_pile
            brick_from = "discard"
        elif path_choose in ('M','m'):
            is_choosen_pile = True
            target_pile = main_pile
            brick_from = "main"
        else:
            print("Please follow the rules \n")
    brick = get_top_brick(target_pile)
    print("You picked %s from %s pile" % (brick, brick_from))
    is_skip = input("Do u want to use this brick ? Type 'Y' or 'N' to skip to turn\n")
    if is_skip in ('N','n'):
        return tower
    elif is_skip in ('Y','y'):
        valid = False
        while not valid:
            brick_replaced = input("where do you want to place this brick? type a brick number to replace in your tower\n")
            if brick_replaced.isnumeric():
                brick_replaced = int(brick_replaced)
                if brick_replaced in tower:
                    valid = True
                    train_log(tower, brick, tower.index(brick_replaced))
                    is_replaced = find_and_replace(brick, brick_replaced, tower, discard_pile)
                    if is_replaced:
                        print("You replaced %s with %s" % (brick_replaced, brick))
                else:
                    print("please ensure %s in your tower : %s" % (brick_replaced,tower))
            else:
                print("please input a number")
    return tower

def main():
    (main_piles, discard_piles) = setup_bricks()
    shuffle_bricks(main_piles)
    (computer_tower, human_tower) = deal_initial_bricks(main_piles)
    running = True
    while running:
        computer_tower = computer_play(computer_tower,main_piles,discard_piles)
        check_bricks(main_piles, discard_piles)
        if check_tower_blaster(computer_tower):
            running = False
            print("computer win !!!")
            print("computer tower is %s" % computer_tower)
            return 
        human_tower = human_play(human_tower, main_piles, discard_piles)
        check_bricks(main_piles, discard_piles)
        if check_tower_blaster(human_tower):
            running = False
            print("you Win !!!")
            print("Your tower is %s" % human_tower)

if __name__ == '__main__':
    main()
