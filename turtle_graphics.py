"""
ShopImpact Turtle Graphics
Run this file on a computer with a desktop display:
    python turtle_graphics.py

This opens a real Python Turtle window and draws a turtle and a leaf.
Streamlit Community Cloud is headless and cannot open tkinter/Turtle windows.
The deployed Streamlit app therefore uses a cloud-safe SVG fallback illustration.
"""
import turtle

screen = turtle.Screen()
screen.title("ShopImpact - Turtle Eco Badge")
screen.bgcolor("#f4f8ef")
screen.setup(width=720, height=520)

pen = turtle.Turtle()
pen.speed(0)
pen.pensize(3)

def filled_circle(x, y, radius, color, outline="#28563b"):
    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()
    pen.color(outline, color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()

# Shell
filled_circle(-30, -15, 105, "#78a96f")
# Shell pattern
pen.color("#dcebcf")
pen.pensize(4)
for start, end in [((-30, -15), (-30, 88)), ((-30, -15), (-120, -15)),
                   ((-30, -15), (60, -15)), ((-30, -15), (-95, 55)),
                   ((-30, -15), (35, 55)), ((-30, -15), (-95, -82)),
                   ((-30, -15), (35, -82))]:
    pen.penup(); pen.goto(start); pen.pendown(); pen.goto(end)

# Head and feet
filled_circle(105, 5, 43, "#a5c985")
for x, y in [(-115, -120), (45, -120), (-115, 65), (45, 65)]:
    filled_circle(x, y, 23, "#8dbd76")

# Eyes and smile
filled_circle(92, 18, 4, "#183c2d", "#183c2d")
filled_circle(119, 18, 4, "#183c2d", "#183c2d")
pen.penup(); pen.goto(94, -2); pen.setheading(-45); pen.pendown()
pen.color("#183c2d"); pen.pensize(3); pen.circle(18, 90)

# Leaf above the turtle
pen.penup(); pen.goto(-5, 150); pen.setheading(55); pen.pendown()
pen.color("#4e8a58", "#a7c987")
pen.begin_fill()
pen.circle(48, 90)
pen.left(90)
pen.circle(48, 90)
pen.end_fill()
pen.penup(); pen.goto(-5, 150); pen.pendown()
pen.color("#4e8a58"); pen.goto(35, 215)

# Caption
pen.penup(); pen.goto(0, -220); pen.color("#24543a")
pen.write("SHOPIMPACT  •  SMALL CHOICES, GREENER TOMORROWS",
          align="center", font=("Arial", 15, "bold"))
pen.hideturtle()
screen.mainloop()
