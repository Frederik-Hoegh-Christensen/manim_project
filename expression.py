from manim import *


def create_arithmetic_expression(expression_list=None):
    if expression_list is None:
        expression_list = [
            "(", "(", "3", "+", "50", "-", "(", "7", "+", "8", ")", ")", ")"]

    expression_objects = [MathTex(e) for e in expression_list]
    expression_group = VGroup(*expression_objects).arrange(RIGHT, buff=0.1)
    expression_group.to_edge(UP)
    return expression_group
