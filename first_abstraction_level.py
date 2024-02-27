from manim import *
from utils import *


class FirstAbstractionLevel(Scene):
    def construct(self):
        line = Line(start=[- config.frame_width, config.frame_height/3, 0],
                    end=[config.frame_width, config.frame_height/3, 0], stroke_width=4)
        self.add(line)
        self.wait(1)
        self.expression_list = [
            "(", "(", "3", "+", "50", ")", "-", "(", "7", "+", "8", ")", ")", "+"
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
        self.wait(1)
        #self.play(Write(self.expression_group))
        #self.wait(1)
        expression_target_pos_1 = (self.expression_group.get_width() / 2) * 8
        
        self.play(self.expression_group.animate.scale(8).shift(LEFT * expression_target_pos_1))
        expression_target_pos_2 = self.expression_group.get_width()
        self.wait(1)
        self.play(self.expression_group.animate.shift(RIGHT * expression_target_pos_2))
        self.wait(5)
        
        operand_stack = Text('Operandstack', font_size=24)
        operand_stack.move_to(2 * UP + 5 * LEFT)
        operator_stack = Text('Operatorstack', font_size=24)
        operator_stack.move_to(2 * UP + 5 * RIGHT)
        self.play(Write(operand_stack))
        self.play(Write(operator_stack))

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
            vo.tex = self.expression_group[0]
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

        def shift_expression_left():
            
            move_left_range = self.expression_group[0].get_width()
            self.expression_group.shift(LEFT * move_left_range)

        for i in range(len(self.expression_list)):
            
            next_elem = self.expression_group[0]
            next_str = self.expression_list[self.counter]
            # if (self.counter >= len(self.expression_group)):
            #     self.wait(2)
            #     break

            if (self.expression_list[self.counter] == "("):
                self.play(FadeOut(self.expression_group[0]))
                self.expression_group.remove(self.expression_group[0])
                self.counter += 1

            elif (self.expression_list[self.counter] == ")"):

                self.play(FadeOut(self.expression_group[0]))
                eval()
                self.expression_group.remove(self.expression_group[0])
                self.counter += 1

            elif (self.expression_list[self.counter] == "+" or self.expression_list[self.counter] == "-"):
                push_ope()
                self.expression_group.remove(self.expression_group[0])
                self.counter += 1

            elif int(self.expression_list[self.counter]):
                push_num(next_elem, next_str)
                self.expression_group.remove(self.expression_group[0])
                self.counter += 1

            if (len(self.expression_group) == 0):
                self.wait(2)
                break
            shift_expression_left()

            
