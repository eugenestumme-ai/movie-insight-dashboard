"""
Movie Insight Dashboard (Command-Line Edition)
Author: Eugene Stumme
Description: A command-line Python application that loads movie data from movies.csv,
calculates summary statistics, filters movies by rating or release year, generates
Seaborn/Matplotlib visualizations, and exports filtered results to CSV.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(filename="movies.csv"):
    """Loads the movie dataset from a CSV file into a Pandas DataFrame."""
    try:
        df = pd.read_csv(filename)
        print(f"Successfully loaded '{filename}' ({len(df)} movies found).")
        return df
    except FileNotFoundError:
        print(f"Error: '{filename}' not found. Please ensure it is in the project folder.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return pd.DataFrame()


def show_statistics(df):
    """Calculates and displays general statistics using a dictionary and Pandas methods."""
    print("\n" + "=" * 45)
    print("             MOVIE STATISTICS")
    print("=" * 45)

    # Finding top-rated and highest-grossing movies
    top_rated_row = df.loc[df['rating'].idxmax()]
    highest_rev_row = df.loc[df['revenue'].idxmax()]

    # Storing statistics in a dictionary (demonstrates dictionary usage)
    stats = {
        "Total Movies in Dataset": len(df),
        "Average Rating": f"{df['rating'].mean():.2f} / 10",
        "Highest-Rated Movie": f"{top_rated_row['title']} ({top_rated_row['rating']} - {int(top_rated_row['release_year'])})",
        "Average Budget": f"${df['budget'].mean():,.2f}",
        "Average Revenue": f"${df['revenue'].mean():,.2f}",
        "Highest-Grossing Movie": f"{highest_rev_row['title']} (${highest_rev_row['revenue']:,.2f})"
    }

    for key, value in stats.items():
        print(f"{key:<25}: {value}")
    print("=" * 45)


def filter_movies(df):
    """Allows the user to filter movies by minimum rating, release year, or both."""
    print("\n--- Filter Movies ---")
    print("1. Filter by minimum rating")
    print("2. Filter by minimum release year")
    print("3. Filter by BOTH minimum rating and release year")

    sub_choice = input("Select filter mode (1-3, or press Enter for 3): ").strip()
    if sub_choice not in ['1', '2', '3']:
        sub_choice = '3'

    filtered = df.copy()

    try:
        if sub_choice in ['1', '3']:
            min_rating = float(input("Enter minimum rating (e.g., 7.0): ").strip())
            filtered = filtered[filtered['rating'] >= min_rating]

        if sub_choice in ['2', '3']:
            min_year = int(input("Enter minimum release year (e.g., 2010): ").strip())
            filtered = filtered[filtered['release_year'] >= min_year]

    except ValueError:
        print("\n[!] Invalid input. Please enter valid numbers for rating and year.")
        return pd.DataFrame()

    print(f"\nFound {len(filtered)} movies matching your criteria:")
    if not filtered.empty:
        print("-" * 65)
        # Display the filtered DataFrame cleanly without index numbers
        print(filtered.to_string(index=False))
        print("-" * 65)
    else:
        print("No movies matched those exact filters. Try lowering your rating or year.")

    return filtered


def visualize_data(df):
    """Creates and saves a Rating Histogram and a Budget vs. Revenue Scatter Plot."""
    print("\n--- Creating Visualizations ---")
    sns.set_theme(style="whitegrid")

    # 1. Histogram of Movie Ratings
    plt.figure(figsize=(8, 5))
    sns.histplot(df['rating'], bins=15, kde=True, color='royalblue', edgecolor='black')
    plt.title("Distribution of Movie Ratings", fontsize=14, fontweight='bold')
    plt.xlabel("Rating", fontsize=12)
    plt.ylabel("Number of Movies", fontsize=12)
    plt.tight_layout()
    plt.savefig("rating_histogram.png", dpi=300)
    print("Saved 'rating_histogram.png' to project folder.")
    print("Displaying Rating Histogram... (Close the plot window to view the next chart)")
    plt.show()

    # 2. Budget vs. Revenue Scatter Plot
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x='budget',
        y='revenue',
        hue='rating',
        palette='viridis',
        s=90,
        alpha=0.85
    )
    plt.title("Movie Budget vs. Revenue", fontsize=14, fontweight='bold')
    plt.xlabel("Budget ($)", fontsize=12)
    plt.ylabel("Revenue ($)", fontsize=12)
    plt.legend(title="Rating", loc="upper left")
    plt.tight_layout()
    plt.savefig("budget_vs_revenue.png", dpi=300)
    print("Saved 'budget_vs_revenue.png' to project folder.")
    print("Displaying Budget vs. Revenue Plot... (Close the plot window to return to menu)")
    plt.show()


def save_filtered_data(filtered_df):
    """Saves the filtered DataFrame to a CSV file (defaults to filtered_movies.csv)."""
    if filtered_df is None or filtered_df.empty:
        print("\n[!] No filtered movies to save. Please run Option 2 (Filter Movies) first.")
        return

    filename = input("Enter filename to save filtered results (press Enter for 'filtered_movies.csv'): ").strip()
    if not filename:
        filename = "filtered_movies.csv"
    elif not filename.endswith(".csv"):
        filename += ".csv"

    try:
        filtered_df.to_csv(filename, index=False)
        print(f"Success! {len(filtered_df)} filtered movies saved to '{filename}'.")
    except Exception as e:
        print(f"Error saving file: {e}")


def main():
    """Main function running the interactive command-line dashboard loop."""
    df = load_data("movies.csv")
    if df.empty:
        return

    filtered_df = None

    # Storing menu options in a list (demonstrates list usage)
    menu_options = [
        "1. View General Statistics",
        "2. Filter Movies (by Rating or Release Year)",
        "3. Visualize Data (Histogram & Scatter Plot)",
        "4. Save Filtered Results to CSV",
        "5. Exit"
    ]

    while True:
        print("\n" + "=" * 40)
        print("      MOVIE INSIGHT DASHBOARD")
        print("=" * 40)
        for option in menu_options:
            print(option)
        print("=" * 40)

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            show_statistics(df)
        elif choice == '2':
            filtered_df = filter_movies(df)
        elif choice == '3':
            visualize_data(df)
        elif choice == '4':
            save_filtered_data(filtered_df)
        elif choice == '5':
            print("Thank you for using the Movie Insight Dashboard. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()