import turtle

def initialize_turtle():
    """Set up the turtle graphics environment"""
    window = turtle.Screen()
    window.title("Original Recursive Tree Generator")
    window.bgcolor("white")
    
    artist = turtle.Turtle()
    artist.speed('fastest')
    artist.color("brown")
    artist.left(90)  # Point upward
    artist.penup()
    artist.goto(0, -250)  # Start at bottom center
    artist.pendown()
    
    return artist, window

def draw_branch(turtle_obj, length, width):
    """Draw a single branch with specified length and width"""
    turtle_obj.pensize(width)
    turtle_obj.forward(length)

def grow_tree(turtle_obj, branch_len, left_angle, right_angle, shrink_factor, depth, width):
    """
    Recursively draw a tree pattern
    Original implementation by Darshan
    """
    if depth <= 0 or branch_len < 6:
        # Draw leaf at the end of branches
        turtle_obj.color("green")
        turtle_obj.stamp()
        turtle_obj.color("brown")
        return
    
    # Draw the main branch
    draw_branch(turtle_obj, branch_len, width)
    
    # Remember current position and heading
    current_pos = turtle_obj.position()
    current_heading = turtle_obj.heading()
    
    # Right branch
    turtle_obj.right(right_angle)
    grow_tree(turtle_obj, branch_len * shrink_factor, left_angle, right_angle, 
             shrink_factor, depth-1, width*0.8)
    
    # Return to main branch position
    turtle_obj.penup()
    turtle_obj.goto(current_pos)
    turtle_obj.setheading(current_heading)
    turtle_obj.pendown()
    
    # Left branch
    turtle_obj.left(left_angle)
    grow_tree(turtle_obj, branch_len * shrink_factor, left_angle, right_angle, 
             shrink_factor, depth-1, width*0.8)
    
    # Return to main branch position
    turtle_obj.penup()
    turtle_obj.goto(current_pos)
    turtle_obj.setheading(current_heading)
    turtle_obj.pendown()

def get_user_input():
    """Collect parameters from the user with validation"""
    while True:
        try:
            print("\nCustom Tree Generator Parameters:")
            left_angle = float(input("Left branch angle (15-45 degrees recommended): "))
            right_angle = float(input("Right branch angle (15-45 degrees recommended): "))
            start_len = float(input("Initial branch length (50-200 pixels recommended): "))
            depth = int(input("Recursion depth (3-8 recommended): "))
            shrink = float(input("Branch shrink factor (0.5-0.9 recommended): "))
            
            if not (0 < shrink < 1):
                raise ValueError("Shrink factor must be between 0 and 1")
            if depth <= 0:
                raise ValueError("Depth must be positive")
                
            return left_angle, right_angle, start_len, depth, shrink
            
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def main():
    """Main program execution"""
    print("=== Original Recursive Tree Generator ===")
    print("Created independently")
    
    # Set up drawing environment
    artist, canvas = initialize_turtle()
    artist.shape("turtle")
    
    # Get user parameters
    left, right, length, depth, shrink = get_user_input()
    
    # Draw the tree
    initial_width = max(5, length/10)
    grow_tree(artist, length, left, right, shrink, depth, initial_width)
    
    # Finalize
    artist.hideturtle()
    canvas.exitonclick()

if __name__ == "__main__":
    main()