from manim import *

class BinaryTreeInsertion(Scene):
    def construct(self):
        # Create the root node of the binary tree
        root = Circle(radius=0.5, color=BLUE)
        root_value = Text("5", font_size=24).move_to(root.get_center())
        self.add(root, root_value)

        # Create the left and right child nodes
        left_child = Circle(radius=0.5, color=BLUE)
        left_child_value = Text("3", font_size=24).move_to(left_child.get_center())
        left_child.next_to(root, LEFT * 2)

        right_child = Circle(radius=0.5, color=BLUE)
        right_child_value = Text("7", font_size=24).move_to(right_child.get_center())
        right_child.next_to(root, RIGHT * 2)

        # Animate the appearance of the left and right children
        self.play(
            Create(left_child), Create(left_child_value),
            Create(right_child), Create(right_child_value),
            run_time=2
        )

        # Animate moving the left and right children into place from the root
        self.play(
            left_child.animate.move_to(root.get_center() + LEFT * 2),
            right_child.animate.move_to(root.get_center() + RIGHT * 2),
            left_child_value.animate.move_to(left_child.get_center()),
            right_child_value.animate.move_to(right_child.get_center()),
            run_time=2
        )

        # Insert a new value (e.g., 2) into the tree
        new_node = Circle(radius=0.5, color=RED)
        new_node_value = Text("2", font_size=24).move_to(new_node.get_center())
        new_node.next_to(left_child, LEFT * 2)

        # Animate the new node appearing and moving into its correct position
        self.play(
            Create(new_node), Create(new_node_value),
            new_node.animate.move_to(left_child.get_center() + LEFT * 2),
            new_node_value.animate.move_to(new_node.get_center()),
            run_time=2
        )

        # Transition to show the updated tree structure after insertion
        self.play(
            FadeIn(new_node), FadeIn(new_node_value),
            run_time=1
        )

        # Hold the final tree structure
        self.wait(2)

