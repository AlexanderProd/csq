from matplotlib.colors import LinearSegmentedColormap


ironbow = LinearSegmentedColormap.from_list(
    "Ironbow",
    [(0, 0, 0), (0.13, 0, 0.55), (0.8, 0, 0.47), (1, 0.84, 0), (1, 1, 1)],
    N=100,
)
red_green_blue = LinearSegmentedColormap.from_list(
    "Red Green Blue", [(1, 0, 0), (0, 1, 0), (0, 0, 1)], N=100
)
blue_green_red = LinearSegmentedColormap.from_list(
    "Blue, Green, Red", [(0, 0, 1), (0, 1, 0), (1, 0, 0)], N=100
)
cold_red = LinearSegmentedColormap.from_list("Cold Red", [(1, 0, 0), (0, 0, 0)], N=100)
red_hot = LinearSegmentedColormap.from_list("Cold Red", [(0, 0, 0), (1, 0, 0)], N=100)
green_hot = LinearSegmentedColormap.from_list("Cold Red", [(0, 0, 0), (0, 1, 0)], N=100)
cold_red_boost = LinearSegmentedColormap.from_list(
    "Cold Red Boost", [(0.76, 0, 0), (0, 0, 0)], N=100
)
cold_green = LinearSegmentedColormap.from_list(
    "Cold Green", [(0, 1, 0), (0, 0, 0)], N=100
)
cold_green_boost = LinearSegmentedColormap.from_list(
    "Cold Green Boost", [(0, 0.76, 0), (0, 0.3, 0), (0, 0, 0)], N=100
)
hottest = LinearSegmentedColormap.from_list(
    "Hottest", [(0, 0, 0), (0.5, 0.5, 0.5), (1, 1, 0)], N=100
)
