import matplotlib.pyplot as plt

def reverse_int(num: int) -> int:
    """
    Returns the reverse of the integer 'num' using integer operations.
    """
    rev = 0
    while num > 0:
        rev = rev * 10 + (num % 10)
        num //= 10
    return rev

def is_palindrome(num: int) -> bool:
    """
    Checks if 'num' is a palindrome by comparing with its reverse (integer-based).
    """
    if num < 0:
        return False
    original = num
    rev = 0
    while num > 0:
        rev = rev * 10 + (num % 10)
        num //= 10
    return rev == original

def palindrome_iterations(n: int, max_iter: int = 500) -> int:
    """
    Returns the number of reverse-and-add iterations needed for 'n' to become a palindrome,
    or 'max_iter' if no palindrome is found within that limit.
    """
    current = n
    for i in range(1, max_iter + 1):
        current += reverse_int(current)
        if is_palindrome(current):
            return i  # Return the iteration at which a palindrome was found
    return max_iter  # If no palindrome found by max_iter, return max_iter

def lychrel_graph_save(start: int, end: int, max_iter: int = 500, filename: str = "lychrel_graph.png"):
    """
    1. Calculates how many iterations each number in [start, end] takes to reach a palindrome 
       (or max_iter if none found).
    2. Plots the data as a single graph.
    3. Saves the graph to 'filename'.
    4. Prints each number's iteration count.
    5. Collects and prints the consecutive differences for numbers that did not reach a palindrome.
    6. Closes the plot (does not stay open).
    """
    x_vals = []
    y_vals = []

    # We'll store numbers that never hit a palindrome within max_iter
    no_palindrome_nums = []

    # 1. Compute iteration counts for each number in the range
    for n in range(start, end + 1):
        iters_needed = palindrome_iterations(n, max_iter=max_iter)
        x_vals.append(n)
        y_vals.append(iters_needed)

        if iters_needed == max_iter:
            no_palindrome_nums.append(n)

    # 2 & 3. Create and save the final plot
    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, "bo-", markersize=4)
    plt.xlabel("Number (n)")
    plt.ylabel("Iterations to Palindrome")
    plt.title(f"Lychrel Graph: n from {start} to {end} (up to {max_iter} iterations)")
    plt.grid(True)

    # Save the figure to a file (no interactive display)
    plt.savefig(filename)
    plt.close()  # Close the figure so it doesn't remain open

    # 4. Print iteration counts for each number
    print(f"Iteration counts for numbers from {start} to {end} (max_iter={max_iter}):\n")
    for n_val, iteration_val in zip(x_vals, y_vals):
        if iteration_val == max_iter:
            print(f"Number {n_val}: did NOT reach a palindrome within {max_iter} iterations.")
        else:
            print(f"Number {n_val}: reached a palindrome after {iteration_val} iterations.")

    # 5. Print the consecutive differences for numbers that did not reach a palindrome
    if len(no_palindrome_nums) > 1:
        differences = [
            no_palindrome_nums[i+1] - no_palindrome_nums[i]
            for i in range(len(no_palindrome_nums) - 1)
        ]
        print("\nNumbers that did NOT reach a palindrome:", no_palindrome_nums)
        print("Differences between consecutive 'no-palindrome' numbers:", differences)
    elif len(no_palindrome_nums) == 1:
        print(f"\nOnly one number did NOT reach a palindrome: {no_palindrome_nums[0]} (no consecutive differences).")
    else:
        print("\nAll numbers reached a palindrome within the given iteration limit!")

if __name__ == "__main__":
    # Example usage:
    # Analyze numbers from 1 through 50, up to 500 iterations each,
    # and save the graph as 'lychrel_graph.png'.
    lychrel_graph_save(start=1, end=500, max_iter=500, filename="lychrel_graph.png")
