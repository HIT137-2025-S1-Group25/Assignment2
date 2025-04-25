"""
This interactive program does the folowing instructions:
- gets paramter inputs from user
- draws a recursive tree using inputs from the user

This program has limitation in:
- screen size
- range of paramters of inputs limitations so that the end result of the drawn tree can fit in the centre of the screen

# Group Name: HIT137_2025_S1_Group25
# Group Members:
# Kushal Mahajan - Student S383488
# Darshan Veerabhadrappa Meti - Student S388441
# Joanna Rivera - Student S392556
# Anmol Singh - Student S385881

"""

import turtle

#Prepare screen canvas and turtle for drawing
def initialize_turtle():
    window = turtle.Screen()
    window.setup(900, 900)
    window.title("Original Recursive Tree Generator")
    window.bgcolor("white")
    artist = turtle.Turtle()
    artist.speed('fastest')
    artist.color("brown")
    artist.hideturtle()
    return artist, window

def gotomainbranch(turtle_obj, pos, heading):
    turtle_obj.penup()
    turtle_obj.goto(pos)
    turtle_obj.setheading(heading)
    turtle_obj.pendown()

def grow_tree(turtle_obj, branch_len, left_angle, right_angle, shrink_factor, depth, width, trunk_size):
 
    if trunk_size != branch_len:
        turtle_obj.color('green')
    else:
        turtle_obj.color('brown')

    # Draw the main branch
    turtle_obj.pensize(width)
    turtle_obj.forward(branch_len)   

    if depth > 0: 
        depth = depth -1
        new_branch = branch_len * shrink_factor
        new_width = width *shrink_factor
 
        # Remember current position and heading
        current_pos = turtle_obj.position()
        current_heading = turtle_obj.heading()
        
        # Right branch
        turtle_obj.right(right_angle)
        grow_tree(turtle_obj, new_branch, left_angle, right_angle, shrink_factor, depth, new_width, trunk_size)
        
        # Return to main branch position
        gotomainbranch(turtle_obj, current_pos, current_heading)

        # Left branch
        turtle_obj.left(left_angle)
        grow_tree(turtle_obj, new_branch, left_angle, right_angle, shrink_factor, depth, new_width, trunk_size)
        
        # Return to main branch position
        gotomainbranch(turtle_obj, current_pos, current_heading)

def get_user_input():
    while True:
        try:
            print("\nCustom Tree Generator Parameters:")
            left_angle = float(input("Left branch angle (15-45 degrees recommended): "))
            right_angle = float(input("Right branch angle (15-45 degrees recommended): "))
            start_len = float(input("Initial branch length (50-200 pixels recommended): "))
            depth = int(input("Recursion depth (3-10 recommended): "))
            shrink = float(input("Branch shrink factor (0.5-0.7 recommended): "))
            
            if not (0 < shrink < 1):
                raise ValueError("Shrink factor must be between 0 and 1")
            if depth <= 0:
                raise ValueError("Depth must be positive")
            if start_len > 200: 
                raise ValueError("Length should be under 200")
            if depth > 10: 
                raise ValueError("recusrive depth should be under 10")

            return left_angle, right_angle, start_len, depth, shrink
            
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def main():
    print("=== Original Recursive Tree Generator ===")
    # Set up drawing environment
    artist, canvas = initialize_turtle()
   
    # Get user parameters
    left, right, length, depth, shrink = get_user_input()
    
    artist.left(90)  # Point upward
    artist.penup()
    artist.goto(0, -length*1.5)  # Start at bottomish
    artist.pendown()

    # Draw the tree
    initial_width = max(5, length/10)
    grow_tree(artist, length, left, right, shrink, depth,  initial_width, length)
    
    # Finalize
    artist.hideturtle()
    canvas.exitonclick()

if __name__ == "__main__":
    main()
