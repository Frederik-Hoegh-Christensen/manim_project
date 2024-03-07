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


def create_placeholders(n: int):
    res = []
    if n < 1:
        return res

    for i in range(n):
        e = Text("1").set_color(BLACK)
        res.append(e)
    return res

def create_array(n:int, num_stack:VGroup):
    num_list = [e[0].copy() for e in num_stack]
    square_list = VGroup()
    for i in range(n):
        print("i: ", i)
        if i < len(num_list):
            rect = Rectangle(width=0.7, height=0.5)
            num = num_list[i].move_to(rect)
            sq = VGroup(rect, num)
        else:
            sq = VGroup(Rectangle(width=0.7, height=0.5), Text("1").set_color(BLACK))

        square_list.add(sq)

    for i in range (len(square_list)):
        if i == 0:
            square_list[i].move_to(DOWN)
            
        else:
            square_list[i].next_to(square_list[i - 1], RIGHT, buff=0)
    
    return square_list


    


