from manim import *
from expression import create_arithmetic_expression


class FirstAbstractionLevel(Scene):
    def construct(self):
        self.wait(1)
        self.expression_list = [
            "(", "(", "3", "+", "50", "-", "(", "7", "+", "8", ")", ")", ")"]
        self.counter = 0
        self.arrow = None
        self.expression_group = create_arithmetic_expression()
        self.play(Write(self.expression_group))
        self.wait(1)
        self.currNumStack = []
        self.currOperatorStack = []
        self.eval_squares = []

        # Play the operand table and set its entries to color BLACK to show an empty table

        def push_num(tex, str):

            stack_element = tex
            enclosing_square = SurroundingRectangle(
                stack_element, color=BLUE, buff=0.3)

            if self.currNumStack == []:
                target_position = (DOWN * 2) + LEFT * 5  # Adjust as needed

            else:
                temp_element = self.currNumStack[-1]
                # TODO correct the space between stack elements
                target_position = temp_element[1].get_top() + UP * 1
                # target_position = (DOWN * 1) + LEFT * 5

            self.currNumStack.append(
                (stack_element, enclosing_square, str))

            # Animate moving the stack_element and the square to the target position
            self.play(
                stack_element.animate.move_to(target_position),
                enclosing_square.animate.move_to(target_position)
            )

        def push_ope():

            stack_element = self.expression_group[self.counter]
            enclosing_square = SurroundingRectangle(
                stack_element, color=BLUE, buff=0.3)

            if self.currOperatorStack == []:
                target_position = (DOWN * 2) + RIGHT * 5  # Adjust as needed

            else:
                temp_element = self.currOperatorStack[-1]
                # TODO correct the space between stack elements
                target_position = temp_element[1].get_top() + UP * 1
                # target_position = (DOWN * 1) + LEFT * 5

            self.currOperatorStack.append(
                (stack_element, enclosing_square, self.expression_list[self.counter]))

            # Animate moving the stack_element and the square to the target position
            self.play(
                stack_element.animate.move_to(target_position),
                enclosing_square.animate.move_to(target_position)
            )


        def pop_num():
            popped_ele1 = self.currNumStack.pop()
            tex1 = popped_ele1[0]
            square1 = popped_ele1[1]
            str1 = popped_ele1[2]

            if self.eval_squares == []:
                target_position = DOWN + RIGHT * 1
            else:
                target_position = self.eval_squares[-1].get_left() + LEFT

            self.eval_squares.append(square1)
            self.play(
                tex1.animate.move_to(target_position),
                square1.animate.move_to(target_position)
            )

            self.wait(1)
            return int(str1)
        
        def pop_ope():
            popped_ele1 = self.currOperatorStack.pop()
            tex1 = popped_ele1[0]
            square1 = popped_ele1[1]
            str1 = popped_ele1[2]

            if self.eval_squares == []:
                target_position = DOWN + RIGHT * 2
            else:
                target_position = self.eval_squares[-1].get_left() + LEFT

            self.eval_squares.append(square1)
            self.play(
                tex1.animate.move_to(target_position),
                square1.animate.move_to(target_position)
            )

            self.wait(1)
            return str1
           



        def eval():
            # TODO eval stuff

            pop_num()
            # if not self.currNumStack:
            #     # Handle the case when the list is empty

            #     raise ValueError("currNumStack is empty")

            # print("NumStack before first pop:", self.currNumStack)

            # popped_ele = self.currNumStack.pop()

            # num1 = int(popped_ele[2])

            # print("Popped Element 1:", popped_ele)
            # print("numstack after first pop:", self.currNumStack)

            # if not self.currNumStack:
            #     # Handle the case when the list is empty after the first pop
            #     raise ValueError("currNumStack is empty after the first pop")

            # num2 = int(self.currNumStack.pop()[2])
            # ope = self.currOperatorStack.pop()[2]
            # if ope == "+":
            #     result = num2 + num1
            # elif ope == "-":
            #     result = num2 - num1

            # result_string = str(result)
            # tex = MathTex(result_string)

            # return result_string, tex

        for i in range(len(self.expression_group)):
            next_elem = self.expression_group[self.counter]
            next_str = self.expression_list[self.counter]
            if (self.counter >= len(self.expression_group)):
                self.wait(2)
                break

            if (self.expression_list[self.counter] == "("):
                self.counter += 1
                # TODO remove

            elif (self.expression_list[self.counter] == ")"):
                # TODO evaluation
                num1 = pop_num()
                ope = pop_ope()
                num2 = pop_num()
                
                if ope == "+":
                    res_string = str(num2 + num1)
                elif ope == "-":
                    res_string = str(num2 - num1)
                
                # equals_tex = MathTex("=")
                # equals = equals_tex.animate.move_to(self.eval_squares[0].get_right())
                # self.play(FadeIn(equals))
                # self.wait(1)
                
                equals_tex = MathTex("=")
                # Move the equals_tex to the desired position
                equals_tex.next_to(self.eval_squares[0], RIGHT)
                # Then, play the FadeIn animation for equals_tex
                self.play(FadeIn(equals_tex))
                self.wait(1)

                # res_tex = MathTex(res_string)
                # res = res_tex.animate.move_to(equals_tex.get_right())
                # self.play(FadeIn(res))
                res_tex = MathTex(res_string)
                # Position res_tex next to equals_tex
                res_tex.next_to(equals_tex, RIGHT)
                # Play the FadeIn animation for res_tex
                self.play(FadeIn(res_tex))

                push_num(res_tex, res_string)
                self.eval_squares = []


                
                #result_string, tex = eval()
                #push_num(tex, result_string)
                self.counter += 1

            elif (self.expression_list[self.counter] == "+" or self.expression_list[self.counter] == "-"):
                push_ope()
                self.counter += 1

            elif int(self.expression_list[self.counter]):
                push_num(next_elem, next_str)
                self.counter += 1

    #     self.num_table = MathTable([
    #         ["A"],
    #         ["B"],
    #         ["C"],
    #         ["D"]], include_outer_lines=True).to_edge(LEFT)
    #     self.num_table.get_entries((1,1)).set_color(BLACK)
    #     self.num_table.get_entries((2,1)).set_color(BLACK)
    #     self.num_table.get_entries((3,1)).set_color(BLACK)
    #     self.num_table.get_entries((4,1)).set_color(BLACK)
    #     self.play(Create(self.num_table))

    #     # Loop Through all the elements in the expression
    #     for i in range(4):
    #         original = self.get_next_list_elem()

    #         if (self.expression_list[self.counter] == "("):
    #             self.counter += 1
    #             continue
    #         elif (self.expression_list[self.counter] == ")"):
    #             #TODO evaluation
    #             self.counter += 1
    #             continue
    #         elif (self.expression_list[self.counter] == "+" or self.expression_list[self.counter] == "-"):
    #             self.counter += 1
    #             continue

    #         elif int(self.expression_list[self.counter]):
    #             next_num = original.copy().move_to(self.num_table.get_entries((self.counter,1)).get_center()).set_opacity(1)
    #             self.play(ReplacementTransform(self.num_table.get_entries((self.counter,1)), next_num))
    #             self.operator_table = None
    #             self.counter += 1
    #             self.wait(2)

    # def get_next_list_elem(self):
    #     if self.counter < len(self.expression_group):
    #         next_elem = self.expression_group[self.counter]
    #         # Fade the element by reducing its opacity
    #         if self.arrow:
    #             # Move the existing arrow
    #             new_arrow = Arrow(
    #                                 next_elem.get_bottom() + DOWN * 1,  # Start point
    #                                 next_elem.get_bottom(),               # End point
    #                                 buff=0.1,                             # Buffer space between arrow tip and target
    #                                 max_tip_length_to_length_ratio=0.5,
    #                                 max_stroke_width_to_length_ratio=20,                      # Directly setting the tip length
    #                             ).set_color(BLUE)
    #             self.play(Transform(self.arrow, new_arrow))
    #         else:
    #             # Create a new arrow if it doesn't exist
    #             self.arrow = Arrow(
    #                                 next_elem.get_bottom() + DOWN * 1,  # Start point
    #                                 next_elem.get_bottom(),               # End point
    #                                 buff=0.1,                             # Buffer space between arrow tip and target
    #                                 max_tip_length_to_length_ratio=0.5,
    #                                 max_stroke_width_to_length_ratio=20,

    #                             ).set_color(BLUE)
    #             self.play(GrowArrow(self.arrow))
    #         self.play(next_elem.animate.set_opacity(0.2))
    #         # Increment the counter to move to the next element in future calls
    #         return next_elem
    #     else:
    #         print("No more elements to fade.")
