def to_num(num, temp=0):
    num_float = float(num)
    num_int = int(num_float)

    if num_int == num_float:
        return num_int

    return round(num_float, 2)


def operation(a, b, op: str):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    else:
        raise Exception('运算符不正确')


def exp_str2list(exp: str):
    opset = {'+', '-', '*', '/'}  # 运算符集合
    flag = -1
    explist = list()
    for i, char in enumerate(exp):
        if char in opset:  # 若char是运算符
            explist.append(exp[flag + 1:i])
            flag = i
            explist.append(char)
    explist.append(exp[flag + 1:])
    return explist


def handle_first_sub(ops):
    ops_new = list()

    # if len(ops) > 1 and ops[0] == "-":
    #     for k in range(len(ops)):
    #         if k > 0:
    #             if ops[k] == "+":
    #                 ops_new.append("-")
    #             if ops[k] == "-":
    #                 ops_new.append("+")
    #         else:
    #             ops_new.append(ops[k])

    for k in range(len(ops)):
        if k > 0:
            if ops[k - 1] == "-":
                if ops[k] == "+":
                    ops_new.append("-")
                if ops[k] == "-":
                    ops_new.append("+")
            else:
                ops_new.append(ops[k])
        else:
            ops_new.append(ops[k])

    if len(ops_new) == 0:
        return ops
    else:
        return ops_new


def calculate_expression(exp: str):
    opset = {'+', '-', '*', '/'}
    nums = list()
    ops = list()

    explist = exp_str2list(exp)

    for e in explist:
        if e in opset:
            ops.append(e)
        else:
            if len(e) == 0:
                continue

            nums.append(eval(e))

        if ops and ops[-1] in {'*', '/'} and len(nums) == len(ops) + 1:
            op = ops.pop()
            y = nums.pop()
            x = nums.pop()
            nums.append(operation(x, y, op))

    # if len(nums) == 0:
    #     return
    # if len(ops) == 0:
    #     return

    ops = handle_first_sub(ops)

    while ops:
        op = ops.pop()
        y = nums.pop()
        x = nums.pop()
        x_op_y = operation(x, y, op)
        nums.append(x_op_y)

    if len(nums) == 0:
        return None
    else:
        return nums[0]


def calculate_math(string):
    if len(string) <= 2:
        return None

    if string.find("-") == 0:
        string = "0" + string

    math_arr = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "*", "/", "."]

    math_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    math_operation = ["+", "-", "*", "/"]

    flag = True
    for i in range(len(string)):
        if not (string[i] in math_arr):
            flag = False
            break

    if not flag:
        # 有非 数字和运算符
        return None

    flag_num = False
    for i in range(len(string)):
        # 必须包含数字
        if (string[i] in math_num):
            flag_num = True
            break

    flag_operation = False
    for i in range(len(string)):
        # 必须包含运算符
        if (string[i] in math_operation):
            flag_operation = True
            break

    if flag_num and flag_operation:
        result = None
        try:
            result = calculate_expression(string)
        except ZeroDivisionError:
            result = "zero"
        except IndexError:
            result = None

        if result is None:
            return None
        else:
            if result == "zero":
                return "除数不能为0"
            else:
                return to_num(result)
    else:
        return None
