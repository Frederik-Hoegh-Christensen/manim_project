from manim import *
from utils import *


class FirstAbstractionLevel(Scene):
    def construct(self):
        self.wait(1)
        self.expression_list = [
            "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")"]
        self.counter = 0
        self.arrow = None
        self.expression_group = create_arithmetic_expression(
            self.expression_list)
        self.play(Write(self.expression_group))
        self.wait(1)
        self.currNumStack = []
        self.currOperatorStack = []
        self.eval_squares = []

        # Play the operand table and set its entries to color BLACK to show an empty table

        def push_num(tex, str):
            vo = Visual_object(tex, str)
            vo.tex = tex
            vo.as_string = str
            vo.square = SurroundingRectangle(
                vo.tex, color=BLUE, buff=0.3)

            if self.currNumStack == []:
                target_position = (DOWN * 2) + LEFT * 5  # Adjust as needed

            else:
                temp_element = self.currNumStack[-1]
                # TODO correct the space between stack elements
                target_position = temp_element.square.get_top() + UP * 1

            self.currNumStack.append(
                vo)

            # Animate moving the stack_element and the square to the target position
            self.play(
                vo.tex.animate.move_to(target_position),
                vo.square.animate.move_to(target_position)
            )

        def push_ope():
            vo = Visual_object()
            vo.tex = self.expression_group[self.counter]
            vo.square = SurroundingRectangle(
                vo.tex, color=BLUE, buff=0.3)
            vo.as_string = self.expression_list[self.counter]

            if self.currOperatorStack == []:
                target_position = (DOWN * 2) + RIGHT * 5  # Adjust as needed

            else:
                temp_element = self.currOperatorStack[-1]
                # TODO correct the space between stack elements
                target_position = temp_element.square.get_top() + UP * 1

            self.currOperatorStack.append(vo)

            # Animate moving the stack_element and the square to the target position
            self.play(
                vo.tex.animate.move_to(target_position),
                vo.square.animate.move_to(target_position)
            )

        def pop_num():
            popped_ele1 = self.currNumStack.pop()

            if self.eval_squares == []:
                target_position = DOWN + RIGHT * 1
            else:
                temp_element = self.eval_squares[-1]
                target_position = temp_element.square.get_left() + LEFT

            self.eval_squares.append(popped_ele1)
            self.play(
                popped_ele1.tex.animate.move_to(target_position),
                popped_ele1.square.animate.move_to(target_position)
            )

            self.wait(1)

            return popped_ele1

        def pop_ope():
            popped_ele1 = self.currOperatorStack.pop()

            if self.eval_squares == []:
                target_position = DOWN + RIGHT * 2
            else:
                temp_element = self.eval_squares[-1]
                target_position = temp_element.square.get_left() + LEFT

            self.eval_squares.append(popped_ele1)
            self.play(
                popped_ele1.tex.animate.move_to(target_position),
                popped_ele1.square.animate.move_to(target_position)
            )

            self.wait(1)
            return popped_ele1

        def eval():

            vo1 = pop_num()
            ope = pop_ope()
            vo2 = pop_num()

            if ope.as_string == "+":
                res_string = str(int(vo2.as_string) +
                                 int(vo1.as_string))
            elif ope.as_string == "-":
                res_string = str(int(vo2.as_string) -
                                 int(vo1.as_string))

            equals_tex = MathTex("=")
            # Move the equals_tex to the desired position

            equals_tex.next_to(self.eval_squares[0].square, RIGHT)
            # Then, play the FadeIn animation for equals_tex
            self.play(FadeIn(equals_tex))
            self.wait(1)
            res_tex = MathTex(res_string)

            res_tex.next_to(equals_tex, RIGHT)

            self.play(FadeIn(res_tex))

            push_num(res_tex, res_string)

            self.play(FadeOut(
                equals_tex,
                vo1.tex, vo1.square,
                ope.tex, ope.square,
                vo2.tex, vo2.square
            ))
            self.eval_squares = []

        for i in range(len(self.expression_group)):
            next_elem = self.expression_group[self.counter]
            next_str = self.expression_list[self.counter]
            if (self.counter >= len(self.expression_group)):
                self.wait(2)
                break

            if (self.expression_list[self.counter] == "("):
                self.play(FadeOut(self.expression_group[self.counter]))
                self.counter += 1

            elif (self.expression_list[self.counter] == ")"):

                self.play(FadeOut(self.expression_group[self.counter]))
                eval()

                self.counter += 1

            elif (self.expression_list[self.counter] == "+" or self.expression_list[self.counter] == "-"):
                push_ope()
                self.counter += 1

            elif int(self.expression_list[self.counter]):
                push_num(next_elem, next_str)
                self.counter += 1
