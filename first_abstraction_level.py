from manim import *
from expression import create_arithmetic_expression


class FirstAbstractionLevel(Scene):
    def construct(self):
        self.wait(1)
        self.expression_list = [
            "(", "3", "+", "5", "-", "(", "7", "+", "8", ")", ")"]
        self.counter = 0
        self.arrow = None
        self.expression_group = create_arithmetic_expression()
        self.play(Write(self.expression_group))
        self.wait(1)
        self.currNumStack = []
        self.currOperatorStack = []

        # Play the operand table and set its entries to color BLACK to show an empty table

        def push():

            # stack_element = VGroup(rect, text).shift(UP*self.stack_height)
            stack_element = self.expression_group[self.counter]

            if (self.expression_list[self.counter] == "("):
                self.counter += 1

            elif (self.expression_list[self.counter] == ")"):
                # TODO evaluation
                self.counter += 1

            elif (self.expression_list[self.counter] == "+" or self.expression_list[self.counter] == "-"):
                self.counter += 1

            elif int(self.expression_list[self.counter]):

                enclosing_square = SurroundingRectangle(
                    stack_element, color=BLUE, buff=0.5)

                if self.currNumStack == []:
                    target_position = (DOWN * 2) + LEFT * 5  # Adjust as needed

                else:
                    temp_element = self.currNumStack.pop()
                    temp_position = temp_element  # get top
                    target_position = (DOWN * 1) + LEFT * 5

                self.currNumStack.append((stack_element, enclosing_square))
                self.counter += 1

                # Animate moving the stack_element and the square to the target position
                self.play(
                    stack_element.animate.move_to(target_position),
                    enclosing_square.animate.move_to(target_position)
                )
                # self.play(Create(stack_element))
                # self.play(Create(enclosing_square))

        push()
        self.wait(1)
        push()
        self.wait(1)
        push()
        self.wait(1)
        push()
        self.wait(1)
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
