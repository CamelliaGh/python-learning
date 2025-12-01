import streamlit as sl
import time
from monty_hall import simulate_monty_hall

sl.title("Monty Hall Simulation")
sl.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Monty_open_door.svg/1200px-Monty_open_door.svg.png", width=400)

# Get number of games to simulate
num_games = sl.number_input(
    "Enter number of games to simulate", min_value=10, max_value=1000, value=100
)

# Create two columns for side-by-side charts
col1, col2 = sl.columns(2)

col1.subheader("Win Percentage Without Switching")
chart1 = col1.line_chart(x=None, y=None, width=400, height=400)
chart1.add_rows([1.0])  # Initialize chart y-axis

col2.subheader("Win Percentage With Switching")
chart2 = col2.line_chart(x=None, y=None, width=400, height=400)
chart2.add_rows([1.0])  # Initialize chart y-axis

if sl.button("Run Simulation"):
    # Track cumulative wins
    wins_no_switch = 0
    wins_switch = 0

    for i in range(1, num_games + 1):
        # Simulate one game and get win results
        num_wins_without_switching, num_wins_with_switching = simulate_monty_hall(
            1)

        # Update cumulative counts
        wins_no_switch += num_wins_without_switching
        wins_switch += num_wins_with_switching

        # Calculate win rate and update charts
        chart1.add_rows([wins_no_switch / i])
        chart2.add_rows([wins_switch / i])
        time.sleep(0.01)  # Small delay for visualization
