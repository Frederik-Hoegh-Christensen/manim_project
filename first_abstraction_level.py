from manim import *
from utils import *
import copy


class FirstAbstractionLevel(Scene):
    def construct(self):
        line = Line(start=[- config.frame_width, config.frame_height/3, 0],
                    end=[config.frame_width, config.frame_height/3, 0], stroke_width=4)
        self.add(line)
        self.wait(1)
        self.expression_list = [
            "(", "1", "+", "5", ")"
            # "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")", "+",
            # "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")", "+",
            # "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")", "+",
            # "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")", "+",
            # "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")", "+",
            # "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")", "+",
            # "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")", "+",
            # "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")"
        ]
        self.counter = 0
        self.arrow = None
        self.expression_group = create_arithmetic_expression(
            self.expression_list)
        self.expression_group.scale(0.1)
        self.add(self.expression_group)
        self.wait(0.5)

        expression_target_pos_1 = (self.expression_group.get_width() / 2) * 8

        self.play(self.expression_group.animate.scale(
            8).shift(LEFT * expression_target_pos_1))
        expression_target_pos_2 = self.expression_group.get_width()
        self.wait(0.5)
        self.play(self.expression_group.animate.shift(
            RIGHT * expression_target_pos_2))
        self.wait(0.5)

        # operand_stack = Text('Operandstack', font_size=24)
        # operand_stack.move_to(2 * UP + 5 * LEFT)
        # operator_stack = Text('Operatorstack', font_size=24)
        # operator_stack.move_to(2 * UP + 5 * RIGHT)
        # self.play(Write(operand_stack))
        # self.play(Write(operator_stack))
        arrow_end = self.expression_group.get_left()
        arrow_start = arrow_end + LEFT
        arrow = Arrow(start=arrow_start, end=arrow_end, buff=0.2)
        # self.play(FadeIn(arrow))

        self.currNumStack = []
        self.testStack = VGroup()
        self.currOperatorStack = []
        self.eval_squares = []

        # Play the operand table and set its entries to color BLACK to show an empty table

        def push_num(tex):
            vo = Visual_object(tex=tex)
            vo.square = SurroundingRectangle(
                vo.tex, color=BLUE, buff=0.3)

            # if self.testStack.submobjects == []:
            #     # (DOWN * 2) + LEFT * 5  # Adjust as needed
            #     target_position = corner

            # else:
            #     temp_element = self.testStack.submobjects[-1]

            #     # TODO correct the space between stack elements
            #     target_position = temp_element.get_top() + UP * 1
            # if self.currNumStack == []:
            #     target_position = (DOWN * 2) + LEFT * 5  # Adjust as needed

            # else:
            #     temp_element = self.currNumStack[-1]

            #     # TODO correct the space between stack elements
            #     target_position = temp_element.square.get_top() + UP * 1

            # self.currNumStack.append(
            #     vo)

            # vo_copy = copy.deepcopy(self.currNumStack[-1])

            # print("kopien", vo_copy.tex)

            # self.testStack.add(VGroup(vo_copy.tex, vo_copy.square))

            # Remove the original element from the expression, before moving the copy
            # Animate moving the stack_element and the square to the target position
            self.testStack.add(VGroup(vo.tex, vo.square))

            print("Test stak", self.testStack)
            target_position = self.testStack[-1].get_top()
            item_to_move = self.testStack[-1]
            if len(self.testStack) == 1:

                self.play(
                    item_to_move.animate.to_corner(DL + (UP * 0.5))
                    # vo.tex.animate.move_to(target_position),
                    # vo.square.animate.move_to(target_position),
                )
            # self.wait(1)
            else:
                target_position = self.testStack[-2].get_top()

                self.play(
                    item_to_move.animate.move_to(target_position)

                )

            self.testStack.arrange(
                UP).to_corner(DL + (UP * 0.5))
            # self.add(self.testStack)

        def push_ope():
            vo = Visual_object()
            vo.tex = self.expression_group[0]
            vo.square = SurroundingRectangle(
                vo.tex, color=BLUE, buff=0.3)

            if self.currOperatorStack == []:
                target_position = (DOWN * 2) + RIGHT * 5  # Adjust as needed

            else:
                temp_element = self.currOperatorStack[-1]
                # TODO correct the space between stack elements
                target_position = temp_element.square.get_top() + UP * 1

            self.currOperatorStack.append(vo)
            # Remove the original element from the expression, before moving the copy

            # Animate moving the stack_element and the square to the target position
            self.expression_group.remove(self.expression_group[0])
            self.play(
                vo.tex.animate.move_to(target_position),
                vo.square.animate.move_to(target_position)
            )
            self.wait(0.5)

        def pop_num():
            popped_ele1 = self.currNumStack.pop()

            if self.eval_squares == []:
                target_position = DOWN + RIGHT * 1
            else:
                temp_element = self.eval_squares[-1]
                target_position = temp_element.square.get_left() + LEFT

            self.eval_squares.append(popped_ele1)
            self.play(
                popped_ele1.square.animate.move_to(target_position),
                popped_ele1.tex.animate.move_to(target_position)
            )

            self.wait(0.5)

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

            self.wait(0.5)
            return popped_ele1

        def eval():

            vo1 = pop_num()
            ope = pop_ope()
            vo2 = pop_num()
            res_string = ""
            if ope.tex.get_tex_string() == "+":
                res_string = str(int(vo2.tex.get_tex_string()) +
                                 int(vo1.tex.get_tex_string()))
            elif ope.tex.get_tex_string() == "-":
                res_string = str(int(vo2.tex.get_tex_string()) -
                                 int(vo1.tex.get_tex_string()))

            equals_tex = MathTex("=")

            # Move the equals_tex to the desired position

            equals_tex.next_to(self.eval_squares[0].square, RIGHT)
            # Then, play the FadeIn animation for equals_tex
            self.play(FadeIn(equals_tex))
            self.wait(0.5)
            res_tex = MathTex(res_string)

            res_tex.next_to(equals_tex, RIGHT)

            self.play(FadeIn(res_tex))

            push_num(res_tex)

            self.play(FadeOut(
                equals_tex,
                vo1.tex, vo1.square,
                ope.tex, ope.square,
                vo2.tex, vo2.square
            ))
            self.eval_squares = []

        def shift_expression_left():

            move_left_range = self.expression_group[0].get_left()
            shift_vector = arrow_end - move_left_range
            self.play(self.expression_group.animate.shift(shift_vector))
            self.wait(0.5)

        for i in range(len(self.expression_list)):

            next_elem = self.expression_group[0].copy()
            next_str = self.expression_list[self.counter]

            if (self.expression_list[self.counter] == "("):
                self.play(FadeOut(self.expression_group[0]))
                self.expression_group.remove(self.expression_group[0])
                self.counter += 1

            elif (self.expression_list[self.counter] == ")"):

                self.play(FadeOut(self.expression_group[0]))
                # eval()
                self.expression_group.remove(self.expression_group[0])
                self.counter += 1

            elif (self.expression_list[self.counter] == "+" or self.expression_list[self.counter] == "-"):
                push_ope()
                self.counter += 1

            elif int(self.expression_list[self.counter]):
                self.expression_group.remove(self.expression_group[0])
                push_num(next_elem)
                # self.expression_group.remove(self.expression_group[0])
                self.counter += 1

            if (len(self.expression_group) == 0):
                self.wait(1)
                break
            shift_expression_left()
