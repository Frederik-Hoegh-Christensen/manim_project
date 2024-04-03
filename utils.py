import math
from manim import *


def create_arithmetic_expression(expression_list=None):
    if expression_list is None:
        expression_list = [
            "(", "(", "3", "+", "50", "-", "(", "7", "+", "8", ")", ")", ")"]

    expression_objects = [MathTex(e) for e in expression_list]
    expression_group = VGroup(*expression_objects).arrange(RIGHT, buff=0.1)
    expression_group.move_to([0, config.frame_height - 4.6, 0])
    # expression_group.to_edge(UP)
    return expression_group


class Visual_object():
    def __init__(self, tex: MathTex = None, square: SurroundingRectangle = None) -> None:
        self.tex = tex
        self.square = square
        # self.as_string = MathTex(as_string)
        # self.submobjects = [tex, square]

class Main_memory():

    def __init__(self, n: int):
        self.main_mem = create_array(str="main", n=n).move_to([0, -6, 0])
        self.num_array = []
        self.ope_array = []
        self.num_start_index = 0
        self.ope_start_index = 0
        
        #print("Main_length", self.main_mem)

        # for i in range (len(self.main_mem)):
        #     self.helper.add(False)

    def find_s(self, length: int):
        is_free = 0
        for i in range(len(self.main_mem)):
            if (len(self.main_mem[i])) == 1:
                for j in range(length):
                    if (len(self.main_mem[i+j]) == 1):
                        is_free += 1
                    else:
                        is_free = 0
                        break
                    if is_free == (length):
                        print("index", i)
                        return i

        print("no free space")
        return -1

    def insert(self, array: VGroup, array_type : str, index : int=None):
        if index is None:
            index = self.find_s(len(array))
        # length = len(array)
        # if array_type == "num" and len(self.num_array) == length:
        #     index = self.num_start_index

        # elif array_type == "ope" and len(self.ope_array) == length:
        #     index = self.ope_start_index
        # else:
        #     index = self.find_s(length)
        #index = self.find_s(length)
        for i in range(len(array)):
            pos = self.main_mem[index + i].get_center()
            self.main_mem[index +
                          i] = array[i].copy().move_to(self.main_mem[index+i])
            
        if array_type == "ope":
            self.ope_array = array
            self.ope_start_index = index
        elif array_type == "num":
            self.num_array = array
            self.num_start_index = index
        

    def get(self):
        return self.main_mem
    
    def update(self, array : VGroup, array_type : str):
        length = len(array)
        index = self.find_s(length=length)

        if array_type == "num":
            if len(self.num_array) == length:
                index = self.num_start_index
            else:
                for i in range(self.num_start_index, len(self.num_array) + self.num_start_index):
                    self.remove_data(i)

        elif array_type == "ope":
            if len(self.ope_array) == length:
                index = self.ope_start_index
            else:
                for i in range(self.ope_start_index, len(self.ope_array) + self.ope_start_index):
                    self.remove_data(i)

        self.insert(array=array, array_type=array_type, index=index)

        # if array_type == "ope":
        #     self.ope_array = array
        #     self.ope_start_index = index
        # elif array_type == "num":
        #     self.num_array = array
        #     self.num_start_index = index


    def remove_data(self, i : int):
        self.main_mem[i].remove(self.main_mem[i][1])

    def reserve_space(self, n: int):
        # Iterate through the helper array
        for i in range(len(self.helper) - n + 1):
            # Check if the next n elements are all False
            if all(not self.helper[j] for j in range(i, i + n)):
                # Change the next n elements to True
                for j in range(i, i + n):
                    self.helper[j] = True
                # Exit the function after reserving the space
                return True  # Indicates that space was successfully reserved
        
        # Return False if there was not enough space to reserve
        return False
    


def create_placeholders(n: int):
    res = []
    if n < 1:
        return res

    for i in range(n):
        e = Text("1").set_color(BLACK)
        res.append(e)
    return res


def create_array(n: int, str: str, stack: VGroup = VGroup()):

    tex_list = [e[0].copy() for e in stack]
    square_list = VGroup()
    for i in range(n):

        if i < len(tex_list):
            rect = Rectangle(width=0.7, height=0.5)
            tex = tex_list[i].move_to(rect)
            sq = VGroup(rect, tex)
        # TODO consider consuing logic here
        elif str == "main":
            sq = VGroup(Rectangle(width=0.7, height=0.5))
        else:
            sq = VGroup(Rectangle(width=0.7, height=0.5), VMobject(None))

        square_list.add(sq)

    for i in range(len(square_list)):
        if i == 0:
            square_list[i].move_to(DOWN)

        else:
            square_list[i].next_to(square_list[i - 1], RIGHT, buff=0)

    if str == "main":
        print("we entered the loop")
        return square_list

    if len(stack) == 0:

        if str == "num":
            # Hardcoded location for the placement of the number-array

            return square_list.next_to([-6.26111111, -3.75, 0.], DOWN * 2)
        if str == "ope":
            # Hardcoded location for the placement of the opeartor-array
            return square_list.next_to([6.26111111, -3.75, 0.], DOWN * 2)

    return square_list.next_to(stack.get_bottom(), DOWN * 2)


def find_nearest_ceiling_power_of_two(number):
    if number <= 1:
        return 2

    # Check if the number is already a power of two
    if math.log(number, 2).is_integer():
        return int(math.pow(2, math.ceil(math.log(number, 2)) + 1))

    power = math.ceil(math.log(number, 2))
    return int(math.pow(2, power))
