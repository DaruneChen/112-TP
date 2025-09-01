import matplotlib.pyplot as plt
import numpy as np

# Data for the chart
types = ["Beef", "Meat", "Poultry"]
calories = [156.82, 158.7, 118.76]
sodium = [411.1, 408.5, 469]

# X-axis positions for the groups
x = np.arange(len(types))

# Bar width
width = 0.35

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(x - width/2, calories, width, label='Calories (avg)', color='blue')
plt.bar(x + width/2, sodium, width, label='Sodium (avg, mg)', color='orange')

# Add labels and title
plt.title("Figure 2: Average Calories and Sodium Content of Hotdog Types", fontsize=14)
plt.xlabel("Hotdog Type", fontsize=12)
plt.ylabel("Values", fontsize=12)
plt.xticks(x, types)
plt.legend()

# Add values on top of bars
for i in range(len(types)):
    plt.text(x[i] - width/2, calories[i] + 5, f"{calories[i]:.2f}", ha='center', fontsize=10)
    plt.text(x[i] + width/2, sodium[i] + 5, f"{sodium[i]:.1f}", ha='center', fontsize=10)

# Show grid and display the chart
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
