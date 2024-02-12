from manim import *
from expression import create_arithmetic_expression


class FirstAbstractionLevel(Scene):
    def construct(self):
        self.wait(1)
        self.counter = 0
        self.arrow = None
        self.expression_group = create_arithmetic_expression()
        self.play(Write(self.expression_group))
        self.wait(1)
        #Play the operand table
        self.num_table = MathTable([
            ["A"],
            ["B"],
            ["C"],
            ["D"]], include_outer_lines=True).to_edge(LEFT)
        self.num_table.get_entries((0,1)).set_color(BLACK)
        self.num_table.get_entries((1,1)).set_color(BLACK)
        self.num_table.get_entries((2,1)).set_color(BLACK)
        self.num_table.get_entries((3,1)).set_color(BLACK)
        self.play(Create(self.num_table))
        original = self.get_next_list_elem()
        next_num = original.copy().move_to(self.num_table.get_entries((1,1)).get_center()).set_opacity(1)
        self.play(ReplacementTransform(self.num_table.get_entries((1,1)), next_num))
        
        self.operator_table = None


        self.get_next_list_elem()
        self.wait(2)
        self.get_next_list_elem()
        self.wait(2)


    def get_next_list_elem(self):
        if self.counter < len(self.expression_group):
            next_elem = self.expression_group[self.counter]
            # Fade the element by reducing its opacity
            if self.arrow:
                # Move the existing arrow
                new_arrow = Arrow(
                                    next_elem.get_bottom() + DOWN * 1,  # Start point
                                    next_elem.get_bottom(),               # End point
                                    buff=0.1,                             # Buffer space between arrow tip and target
                                    max_tip_length_to_length_ratio=0.5,
                                    max_stroke_width_to_length_ratio=20,                      # Directly setting the tip length
                                ).set_color(BLUE)
                self.play(Transform(self.arrow, new_arrow))
            else:
                # Create a new arrow if it doesn't exist
                self.arrow = Arrow(
                                    next_elem.get_bottom() + DOWN * 1,  # Start point
                                    next_elem.get_bottom(),               # End point
                                    buff=0.1,                             # Buffer space between arrow tip and target
                                    max_tip_length_to_length_ratio=0.5,
                                    max_stroke_width_to_length_ratio=20,

                                    
                                ).set_color(BLUE)
                self.play(GrowArrow(self.arrow))
            self.play(next_elem.animate.set_opacity(0.2))
            # Increment the counter to move to the next element in future calls
            self.counter += 1
            return next_elem
        else:
            print("No more elements to fade.")