from Grid import Grid

def main():
    grid: Grid = Grid(
        max_x=10,
        max_y=10,
        grid_spacing=0.5
    )
    grid.plot()

if __name__ == "__main__":
    main()