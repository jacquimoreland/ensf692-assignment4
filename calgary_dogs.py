# calgary_dogs.py
# Jacqui Moreland
#
# A terminal-based application for computing and printing statistics based on given input.

import pandas as pd

# Global variables.
dog_breed_data = pd.DataFrame()
selected_breed = ""
years_top = pd.Series()

def validate_input(input):
    """
    Validate the user input by checking that the input dog breed is in the dataframe.

    Args:
        input: (str) the input string from the user

    Return:
        (boolean) True if the input dog breed is found in the dataframe, otherwise throw
        KeyError with error message saying the dog breed was not found
    """

    global selected_breed
    selected_breed = input.upper()
    # List of all unique dog breeds
    breeds = dog_breed_data.loc[:, "Breed"].unique()
    if selected_breed in breeds:
        return True
    else:
        raise KeyError("Dog breed not found in the data. Please try again.")

def filter_by_breed():
    """
    Creates a new dataframe that only contains entries where the dog breed matches the selected breed
    (determined by the user input)

    Return:
        (pd.DataFrame) dataframe containing entries that have a dog breed == selected breed
    """

    idx = pd.IndexSlice
    mask = dog_breed_data.loc[:, "Breed"] == selected_breed
    entries_of_breed = dog_breed_data.loc[idx[mask, :]]    
    return entries_of_breed

def years_top_breed():
    """
    Calls filter_by_breed to filter through the dataframe and get only entries with the selected dog breed. Gets all the years
    for which there is an entry of the selected breed in the database. Prints the result.
    """

    entries_of_breed = filter_by_breed()
    global years_top
    # Get all unique years where there was an entry of the selected breed. 
    years_top = entries_of_breed.index.get_level_values(level=0).unique() 
    years_top = years_top.get_level_values(level=0)
    years_str = ""
    for i in range(years_top.size):
        years_str = years_str + str(years_top[i]) + " "
    print(f"The {selected_breed} was found in the top breeds for years: {years_str[:-1]}")


def total_num_breed_all_years():
    """
    Calls filter_by_breed to filter through the dataframe and get only entries with the selected dog breed. Sum the total number
    of registrations across all years for the selected breed. 

    Return:
        (int) the total registrations for the selected breed across all years
    """

    entries_of_breed = filter_by_breed()
    total_breed = entries_of_breed.loc[:, "Total"]
    total_breed = total_breed.sum()
    return total_breed


def breed_percentage_by_year(year):
    """
    Confirm that the selected breed has an entry/entries for the passed year value. 
        - If not, print out message saying that the selected breed was not in the top for that year. 
        - If yes, divide the total registration values for the selected breed by the total registration 
        values for all breeds for the given year. Print out the calculated percentage. 
    Args:
        year: (int) the year in question
    """

    if year in years_top:
        # Total number of dogs in given year
        total_all_breeds = dog_breed_data.loc[(year, slice(None)), "Total"]
        total_all_breeds = total_all_breeds.sum()
        # Total number of dogs of selected breed in given year
        entries_of_breed = filter_by_breed()
        total_selected_breed = entries_of_breed.loc[(year, slice(None)), "Total"]
        total_selected_breed = total_selected_breed.sum()
        # Percentage of selected breed out of total numbmer of dogs in given year
        precentage = (total_selected_breed / total_all_breeds) * 100
        print(f"The {selected_breed} was {precentage:.6f}% of top breeds in {year}.")
    else:
        print(f"The {selected_breed} was not in the top breeds in {year}.")


def total_num_all_breeds_all_years():
    """
    Helper function: Get the total number of registrations for all breeds across all years. Return the sum of the totals.  

    Return:
        (int) sum of the total registrations for all breeds across all years
    """
    
    total_all_breeds = dog_breed_data.loc[:, "Total"]
    total_all_breeds = total_all_breeds.sum()
    return total_all_breeds


def breed_percentage_all_years():
    """
    Divide the total registration values for the selected breed by the total registration 
    values for all breeds across all years. Print out the calculated percentage. 
    """
    
    precentage = (total_num_breed_all_years() / total_num_all_breeds_all_years()) * 100
    print(f"The {selected_breed} was {precentage:.6f}% of top breeds across all years.")


def most_popular_months():
    """
    Calls filter_by_breed to filter through the dataframe and get only entries with the selected dog breed.
    Uses groupby to get the count of all the months for which the selected dog breed was listed as a dog breed 
    across all years. 
    
    If multiple months tie for the most times listed in the dataset, then print all those months, otherwise just print
    out the month that was listed the most for the selected breed. 
    """

    entries_of_breed = filter_by_breed()
    without_year = entries_of_breed.droplevel(level=0)
    # Group the data based on month and breed. Breed is already filtered, so gets count 
    # of all month values listed for the selected breed. 
    grouped = without_year.groupby(["Month", "Breed"]).count()
    max_freq = grouped.loc[:, "Total"].max()

    # Create list to contain all months that are equal to max
    max_months = []
    for i in range(grouped.size):
        if (grouped.iloc[i, 0] == max_freq):
            max_months.append(grouped.index[i][0])
    months_str = ""
    for i in range(len(max_months)):
        months_str += str(max_months[i]) + " "
    print(f"Most popular month(s) for {selected_breed} dogs: {months_str[:-1]}\n")


def main():
    # Import data and create a multi-index data frame.
    global dog_breed_data
    dog_breed_data = pd.read_csv('CalgaryDogBreeds.csv', index_col=[0,1])

    print("\nENSF 692 Dogs of Calgary")

    # Prompt the user to input a dog breed. Continue prompting until the input is a valid dog breed name. 
    while True:
        try:
            user_input = input("Please enter a dog breed: ")
            if validate_input(user_input) == True:
                break
        except KeyError as err:
            e = err.args[0]
            print(e)

    # Years dog breed was listed
    years_top_breed()

    # Total num selected breed
    print(f"There have been {total_num_breed_all_years()} {selected_breed} dogs registered total.")

    # Percentage of total each year
    breed_percentage_by_year(2021)
    breed_percentage_by_year(2022)
    breed_percentage_by_year(2023)

    # Percentage of total all years
    breed_percentage_all_years()

    # Most popular months
    most_popular_months()


if __name__ == '__main__':
    main()
