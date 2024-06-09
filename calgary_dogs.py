# calgary_dogs.py
# Jacqui Moreland
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd

# Global variables.
dog_breed_data = pd.DataFrame()
selected_breed = ""

def validate_input(input):
    breeds = dog_breed_data.loc[:, "Breed"].unique()
    global selected_breed
    selected_breed = input.upper()
    if selected_breed in breeds:
        return True
    else:
        raise KeyError("Dog breed not found in the data. Please try again.")

def filter_by_breed():
    # gets me all the entries where Breed == selected breed
    idx = pd.IndexSlice
    mask = dog_breed_data.loc[:, "Breed"] == selected_breed
    entries_of_breed = dog_breed_data.loc[idx[mask, :]]    
    return entries_of_breed

def years_top_breed():
    entries_of_breed = filter_by_breed()
    years_top = entries_of_breed.index.get_level_values(level=0).unique()    # gets all the years
    years_top = years_top.get_level_values(level=0)
    years_str = ""
    for i in range(years_top.size):
        years_str = years_str + str(years_top[i]) + " "
    print(f"The {selected_breed} was found in the top breeds for years: {years_str[:-1]}")


def total_num_breed_all_years():
    # Total number of dogs of selected breed across all years
    entries_of_breed = filter_by_breed()
    total_breed = entries_of_breed.loc[:, "Total"]
    total_breed = total_breed.sum()
    return total_breed


def breed_percentage_by_year(year):
    # Total number of dogs in given year
    #total_all_breeds = dog_breed_data.loc[year, "Total"]
    total_all_breeds = dog_breed_data.loc[(year, slice(None)), "Total"]
    total_all_breeds = total_all_breeds.sum()
    # Total number of dogs of selected breed in given year
    entries_of_breed = filter_by_breed()
    # total_selected_breed = entries_of_breed.loc[(year, "Total")]
    total_selected_breed = entries_of_breed.loc[(year, slice(None)), "Total"]
    total_selected_breed = total_selected_breed.sum()
    # Percentage of selected breed out of total numbmer of dogs in given year
    precentage = (total_selected_breed / total_all_breeds) * 100
    print(f"The {selected_breed} was {precentage:.4f}% of top breeds in {year}.")


def total_num_all_breeds_all_years():
    # Total number of dogs of all breeds across all years
    total_all_breeds = dog_breed_data.loc[:, "Total"]
    total_all_breeds = total_all_breeds.sum()
    return total_all_breeds


def breed_percentage_all_years():
    # Percentage of selected breed out of total numbmer of dogs across all years
    precentage = (total_num_breed_all_years() / total_num_all_breeds_all_years()) * 100
    print(f"The {selected_breed} was {precentage:.4f}% of top breeds across all years.")


def most_popular_months():
    entries_of_breed = filter_by_breed()
    without_year = entries_of_breed.droplevel(level=0)
    grouped = without_year.groupby(["Month", "Breed"]).count()
    max_freq = grouped.loc[:, "Total"].max()

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
            print(err)

    # Data anaylsis stage

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
