from manim import *
from utils import *
import copy


class FirstAbstractionLevel(ZoomedScene):
    def construct(self):
        level = 1
        line = Line(start=[- config.frame_width, config.frame_height/3, 0],
                    end=[config.frame_width, config.frame_height/3, 0], stroke_width=4)
        self.add(line)
        self.wait(1)
        self.expression_list = [

            # "(", "(", "5", "+", "4", "+", "2", "+", "3", "+", "7", "+", "8", "+", "9", ")", ")", ")", ")", "-", "6", "-", "5", "+", "9", ")", "+", "9", "+", "3", "+", "2", "+", "4", "-", "6", "+", "7", ")", "+", "7", ")"
            "(", "3", "+", "10", "+", "5", "+", "5", ")"
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

        # ZOOM
        # self.play(
        #     self.camera.frame.animate.scale(
        #         scale_factor=2, about_point=UP * 2)
        # )

        operand_stack = Text('Operandstack', font_size=20)
        operand_stack.move_to(2 * UP + 6 * LEFT)
        operator_stack = Text('Operatorstack', font_size=20)
        operator_stack.move_to(2 * UP + 6 * RIGHT)
        self.play(Write(operand_stack))
        self.play(Write(operator_stack))
        arrow_end = self.expression_group.get_left()
        arrow_start = arrow_end + LEFT
        arrow = Arrow(start=arrow_start, end=arrow_end, buff=0.2)
        self.play(FadeIn(arrow))

        # self.add(self.num_array)

        # ACTUAL STACKS
        self.num_stack = VGroup()
        self.ope_stack = VGroup()

        self.num_arr_size = 2

        self.currOperatorStack = []
        self.eval_squares = []
        # Arrays
        self.current_number_array = None
        self.current_ope_array = None
        self.main_memory = Main_memory(160)

        # Play the operand table and set its entries to color BLACK to show an empty table

        def push_num(tex):
            vo = Visual_object(tex=tex)
            # vo.tex.font_size = 38.4
            vo.square = SurroundingRectangle(
                vo.tex, color=BLUE, buff=0.3)
            vo.square.stretch_to_fit_width(0.7)

            self.num_stack.add(VGroup(vo.tex, vo.square))

            target_position = self.num_stack[-1].get_top()
            item_to_move = self.num_stack[-1]

            # Variable for control of stack_size according to level
            if level > 1:
                stack_size = item_to_move.animate.scale(0.5).to_corner(
                    DL + (UP * 0.5))
            else:
                stack_size = item_to_move.animate.to_corner(DL+(UP * 0.5))

            if len(self.num_stack) == 1:

                self.play(
                    stack_size
                )

            else:
                # Position at top of the stack

                target_position = self.num_stack[-2].get_top() + \
                    UP * (item_to_move.height / 2)

                # control scaling for move
                if level > 1:
                    stack_move = item_to_move.animate.scale(
                        0.5).move_to(target_position)
                else:
                    stack_move = item_to_move.animate.move_to(target_position)

                self.play(
                    stack_move

                )

            self.num_stack.arrange(
                buff=0,
                direction=UP).to_corner(DL + (UP * 0.5))

            update_array('num')
            if level > 2:
                self.main_memory.update(
                    array=self.current_number_array, array_type="num", level=level)

        def push_ope():
            vo = Visual_object()
            vo.tex = self.expression_group[0]
            vo.square = SurroundingRectangle(
                vo.tex, color=BLUE, buff=0.3)
            vo.square.stretch_to_fit_width(0.7)

            self.ope_stack.add(VGroup(vo.tex, vo.square))

            target_position = self.ope_stack[-1].get_top()
            item_to_move = self.ope_stack[-1]
            if len(self.ope_stack) == 1:

                self.play(
                    item_to_move.animate.scale(0.5).to_corner(DR + (UP * 0.5))
                )

            else:
                # Position at top of the stack
                target_position = self.ope_stack[-2].get_top() + \
                    UP * (item_to_move.height / 2)

                self.play(
                    item_to_move.animate.scale(0.5).move_to(target_position)

                )

            self.ope_stack.arrange(
                buff=0,
                direction=UP).to_corner(DR + (UP * 0.5))

            update_array('ope')
            if level > 2:
                self.main_memory.update(
                    array=self.current_ope_array, array_type="ope", level=level)

        def pop_num():
            original = self.num_stack[-1]
            popped_ele = copy.deepcopy(self.num_stack[-1])
            self.add(popped_ele)
            self.remove(original)
            self.num_stack.remove(original)

            if self.eval_squares == []:
                target_position = RIGHT
            else:
                temp_element = self.eval_squares[-1]
                target_position = temp_element.get_left() + LEFT * 0.5

            self.eval_squares.append(popped_ele[0])
            self.play(
                FadeOut(popped_ele[1])
            )
            self.remove(popped_ele[1])

            index_to_fade_main_mem = self.main_memory.num_start_index + \
                len(self.num_stack)
            index_to_fade_array = len(self.num_stack)
            if level == 3:
                self.play(
                    FadeOut(
                        self.main_memory.main_mem[index_to_fade_main_mem][1]),
                    FadeOut(self.current_number_array[index_to_fade_array][1]),
                    popped_ele[0].animate.move_to(target_position).scale(2)
                )
                self.current_number_array.remove(
                    self.current_number_array[index_to_fade_array][1])
                self.remove(self.current_number_array)
                self.add(self.current_number_array)

            elif level > 1:
                self.play(
                    # FadeOut(self.main_memory.main_mem[index_to_fade_main_mem][1]),
                    FadeOut(self.current_number_array[index_to_fade_array][1]),
                    popped_ele[0].animate.move_to(target_position).scale(2)
                )
                self.current_number_array.remove(
                    self.current_number_array[index_to_fade_array][1])
                self.remove(self.current_number_array)
                self.add(self.current_number_array)
            else:
                self.play(
                    # FadeOut(self.main_memory.main_mem[index_to_fade_main_mem][1]),
                    # FadeOut(self.current_number_array[index_to_fade_array][1]),
                    popped_ele[0].animate.move_to(target_position).scale(2)
                )

            update_array('num')
            if level == 3:
                self.remove(self.main_memory.get())
                self.add(self.main_memory.get())
                self.main_memory.update(
                    array=self.current_number_array, array_type="num", level=level)

            return popped_ele

        def pop_ope():
            original = self.ope_stack[-1]
            popped_ele = copy.deepcopy(original)
            self.add(popped_ele)
            self.remove(original)
            self.ope_stack.remove(original)

            if self.eval_squares == []:
                target_position = RIGHT * 2
            else:
                temp_element = self.eval_squares[-1]
                target_position = temp_element.get_left() + LEFT * 0.5

            self.eval_squares.append(popped_ele[0])
            self.play(FadeOut(popped_ele[1]))
            self.remove(popped_ele[1])

            index_to_fade_main_mem = self.main_memory.ope_start_index + \
                len(self.ope_stack)
            index_to_fade_array = len(self.ope_stack)

            if level == 3:
                self.play(
                    FadeOut(
                        self.main_memory.main_mem[index_to_fade_main_mem][1]),
                    FadeOut(self.current_ope_array[index_to_fade_array][1]),
                    popped_ele[0].animate.move_to(target_position).scale(2)
                )
                self.current_ope_array.remove(
                    self.current_ope_array[index_to_fade_array][1])
                self.remove(self.current_ope_array)
                self.add(self.current_ope_array)

            elif level > 1:
                self.play(
                    # FadeOut(self.main_memory.main_mem[index_to_fade_main_mem][1]),
                    FadeOut(self.current_ope_array[index_to_fade_array][1]),
                    popped_ele[0].animate.move_to(target_position).scale(2)

                )
                self.current_ope_array.remove(
                    self.current_ope_array[index_to_fade_array][1])
                self.remove(self.current_ope_array)
                self.add(self.current_ope_array)

            else:
                self.play(
                    # FadeOut(self.main_memory.main_mem[index_to_fade_main_mem][1]),
                    # FadeOut(self.current_ope_array[index_to_fade_array][1]),
                    popped_ele[0].animate.move_to(target_position).scale(2)

                )

            update_array('ope')
            if level == 3:
                self.remove(self.main_memory.get())
                self.add(self.main_memory.get())
                self.main_memory.update(
                    self.current_ope_array, 'ope', level=level)
            return popped_ele

        def eval():

            vo1 = pop_num()
            ope = pop_ope()
            vo2 = pop_num()
            res_string = ""
            if ope[0].get_tex_string() == "+":
                res_string = str(int(vo2[0].get_tex_string()) +
                                 int(vo1[0].get_tex_string()))
            elif ope[0].get_tex_string() == "-":
                res_string = str(int(vo2[0].get_tex_string()) -
                                 int(vo1[0].get_tex_string()))

            equals_tex = MathTex("=")

            # Move the equals_tex to the desired position

            equals_tex.next_to(self.eval_squares[0], RIGHT)
            # Then, play the FadeIn animation for equals_tex
            self.play(FadeIn(equals_tex))
            self.wait(0.5)
            res_tex = MathTex(res_string)

            res_tex.next_to(equals_tex, RIGHT)
            res_tex.font_size = 38.4
            self.play(FadeIn(res_tex))

            push_num(res_tex)

            self.play(FadeOut(
                equals_tex,
                vo1[0],  # .tex, vo1.square,
                ope[0],  # .tex, ope.square,
                vo2[0]  # .tex, vo2.square
            ))
            self.eval_squares = []

        def shift_expression_left():

            move_left_range = self.expression_group[0].get_left()
            shift_vector = arrow_end - move_left_range
            self.play(self.expression_group.animate.shift(shift_vector))
            self.wait(0.5)

        def update_array(str: str):

            # Do nothing if first abstraction level
            if level == 1:
                return

            if str == 'num':
                stack = self.num_stack
                array = self.current_number_array

            if str == 'ope':
                stack = self.ope_stack
                array = self.current_ope_array

            array_size = 2
            print("#################\narray:", array)
            if (array):
                array_size = len(array)
                self.remove(array)

            current_elements = VGroup()
            # The current array
            array = create_array(
                array_size, str, stack)

            for elem in array:
                elem[1].scale(2)

            self.add(array)

            # Doubling of array-size
            if (array_size == len(stack)):
                self.main_memory.update(
                    array=array, array_type=str, level=level)
                array_size = array_size * 2
                tmp_arr = create_array(
                    array_size, str).next_to(array, DOWN)
                self.wait(0.5)
                self.add(tmp_arr)

                # Indicate tmp array and the location in MM
                if level == 3:
                    length = len(tmp_arr)
                    start = self.main_memory.find_s(length)
                    end = start + length
                    mm_data = copy.deepcopy(self.main_memory.get()[start: end])
                    self.main_memory.get()[start: end].set_color(BLACK)
                    self.add(mm_data)
                    self.play(
                        Indicate(tmp_arr),
                        Indicate(mm_data),
                        run_time=2
                    )
                    self.main_memory.get()[start: end].set_color(WHITE)
                    self.remove(mm_data)
                for i in range(len(stack)):
                    current_elements.add(array[i][1].copy())

                zipped = zip(current_elements,
                             tmp_arr[0:len(current_elements)])

                elems, animations = self.main_memory.get_animation_move(
                    len(stack), str, array_size, level=level)

                if animations:
                    self.add(elems)
                    for i, (elem, target) in enumerate(zipped):
                        self.play(elem.animate.move_to(target), animations[i])
                else:
                    for elem, target in zipped:
                        self.play(elem.animate.move_to(target))

                self.wait(0.5)
                self.play(FadeOut(array))
                target_p = array.get_center()
                self.remove(array, tmp_arr, *current_elements)
                array = create_array(
                    array_size, str, stack).move_to(tmp_arr)
                for elem in array:
                    elem[1].scale(2)
                self.add(array)
                self.play(array.animate.move_to(target_p))
                self.wait(1)

                if elems:
                    self.remove(elems)

            # Halving of array-size when number of elements is 1/4 of the arraysize
            elif ((array_size / 4) == len(stack)):

                array_size = int(array_size / 2)
                tmp_arr = create_array(
                    array_size, str).next_to(array, DOWN)
                self.wait(0.5)
                self.add(tmp_arr)
                if level == 3:
                    length = len(tmp_arr)
                    start = self.main_memory.find_s(length)
                    end = start + length
                    mm_data = copy.deepcopy(self.main_memory.get()[start: end])
                    self.main_memory.get()[start: end].set_color(BLACK)
                    self.add(mm_data)
                    self.play(
                        Indicate(tmp_arr),
                        Indicate(mm_data),
                        run_time=2
                    )
                    self.main_memory.get()[start: end].set_color(WHITE)
                    self.remove(mm_data)
                for i in range(len(stack)):
                    current_elements.add(array[i][1].copy())

                zipped = zip(current_elements,
                             tmp_arr[0:len(current_elements)])

                elems, animations = self.main_memory.get_animation_move(
                    len(stack), str, array_size, level=level)

                # self.play(*move_elements, *animations)
                if animations:
                    self.add(elems)
                    for i, (elem, target) in enumerate(zipped):
                        self.play(elem.animate.move_to(target), animations[i])
                else:
                    for elem, target in zipped:
                        self.play(elem.animate.move_to(target))

                self.wait(0.5)
                self.play(FadeOut(array))
                target_p = array.get_center()
                self.remove(array, tmp_arr, *current_elements)
                array = create_array(
                    array_size, str, stack).move_to(tmp_arr)
                for elem in array:
                    elem[1].scale(2)
                self.add(array)
                self.play(array.animate.move_to(target_p))

                if elems:
                    self.remove(elems)

            if str == 'num':
                self.current_number_array = array
            if str == 'ope':
                self.current_ope_array = array

        # MAIN LOOP ASG
        for i in range(len(self.expression_list)):
            if i == 4:
                level = 2
                self.play(
                    self.camera.frame.animate.scale(
                        scale_factor=1.3, about_point=UP * 2.5),
                    self.num_stack.animate.scale(
                        0.5).to_corner(DL + (UP * 0.5))
                )
                # for i in range(len(self.num_stack)):
                #     self.play(self.num_stack[i].animate.scale(0.5))

                n_complement = find_nearest_ceiling_power_of_two(
                    len(self.num_stack))
                self.current_number_array = create_array(
                    n_complement, "num", self.num_stack)
                for i in range(len(self.num_stack)):
                    self.current_number_array[i][1].scale(2)

                o_complement = find_nearest_ceiling_power_of_two(
                    len(self.ope_stack))
                self.current_ope_array = create_array(
                    o_complement, "ope", self.ope_stack)
                for i in range(len(self.ope_stack)):
                    self.current_ope_array[i][1].scale(2)

                self.play(
                    FadeIn(
                        self.current_ope_array,
                        self.current_number_array
                    )
                )

            if i == 7:
                level = 3
                self.play(
                    self.camera.frame.animate.scale(
                        scale_factor=1.8, about_point=UP * 2)
                )

                self.wait(0.5)
                (mem, cop), trans = self.main_memory.present()
                self.main_memory.insert(
                    array=self.current_number_array, array_type="num")
                self.main_memory.insert(
                    array=self.current_ope_array, array_type="ope")

                self.wait(0.5)
                self.play(trans)
                self.add(mem, cop)
                self.add(self.main_memory.get())
                self.remove(mem, cop)

                num_start, num_end = self.main_memory.get_numbers()
                ope_start, ope_end = self.main_memory.get_operators()

                # Ensuring that the relevant parts of main_mem become black/invisible while indicating copies of the same parts
                op = self.main_memory.get()[ope_start: ope_end]
                nu = self.main_memory.get()[num_start: num_end]
                op_cop = copy.deepcopy(op)
                num_cop = copy.deepcopy(nu)
                op.set_color(BLACK)
                nu.set_color(BLACK)

                self.add(op_cop, num_cop)

                self.play(
                    Indicate(
                        num_cop, rate_func=there_and_back_with_pause, run_time=2),
                    Indicate(self.current_number_array,
                             rate_func=there_and_back_with_pause, run_time=2)
                )

                self.play(
                    Indicate(
                        op_cop, rate_func=there_and_back_with_pause, run_time=2),
                    Indicate(self.current_ope_array,
                             rate_func=there_and_back_with_pause, run_time=2)

                )
                op.set_color(WHITE)
                nu.set_color(WHITE)
                self.remove(op_cop, num_cop)

            next_elem = self.expression_group[0].copy()

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
                self.expression_group.remove(self.expression_group[0])
                push_num(next_elem)
                self.counter += 1

            if (len(self.expression_group) == 0):
                self.wait(1)
                break
            shift_expression_left()
