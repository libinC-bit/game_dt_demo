class Node:
    def __init__(self, decision_function, left=None, right=None):
        self.decision_function = decision_function
        self.left = left
        self.right = right


#决策树内容
#如果敌人在攻击范围内，优先攻击而不行动
#如果有魔法值，优先使用技能攻击
#如果敌人在攻击范围外，优先向敌人移动
def create_tree():

    node11= Node(lambda state: '向下移动')
    node10= Node(lambda state: '向右移动')
    node9= Node(lambda state: state['敌人在右侧'], left=node10, right=node11)
    node8= Node(lambda state: '向左移动')
    node7= Node(lambda state: state['敌人在左侧'], left=node8, right=node9)
    node6= Node(lambda state: '向上移动')
    node2 = Node(lambda state: state['敌人在上侧'], left=node6, right=node7)
    node5= Node(lambda state: '普通攻击')
    node4= Node(lambda state: '技能攻击')
    node12=Node(lambda state: state['敌人在普通攻击范围内'],left=node5,right=node2)
    node1= Node(lambda state: state['有魔法值'], left=node4, right=node12)
    root = Node(lambda state: state['敌人在技能攻击范围内'], left=node1, right=node12)

    return root

def get_action(tree, state):
    node = tree
    while node.left or node.right:
        #print(node.decision_function(state))
        if node.decision_function(state):
            node = node.left
        else:
            node = node.right

    return node.decision_function(state)
def print_tree(node, indent=0):
    print('  ' * indent + str(node.decision_function.__code__.co_consts))
    if node.left:
        print('  ' * (indent + 1) + 'Y:')
        print_tree(node.left, indent + 2)
    if node.right:
        print('  ' * (indent + 1) + 'N:')
        print_tree(node.right, indent + 2)

#计算树的深度
def tree_depth(node):
    if node==None:
        return 0
    else:
        left_depth=tree_depth(node.left)
        right_depth=tree_depth(node.right)
        return max(left_depth,right_depth)+1

def test():
    state = {'有魔法值': False, '敌人在技能攻击范围内': False,'敌人在普通攻击范围内':True, '技能攻击高': False, '敌人在上侧': False, '敌人在左侧': False, '敌人在右侧': False}
    tree = create_tree()
    print(get_action(tree, state))


def make_decision(state):
    tree = create_tree()
    return get_action(tree, state)


if __name__ == '__main__':
    print_tree(create_tree())
    print(tree_depth(create_tree()))