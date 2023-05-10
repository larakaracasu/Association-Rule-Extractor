# Association Rule Extractor

This project utilizes the Apriori algorithm to generate association rules for the NY Complain Data from 2023. The goal is to analyze the dataset and identify any interesting associations between different attributes, such as the type of crime and the borough/location where it was committed.

## Contributors

- Ulas Alakent - ua2182
- Lara Karacasu - lk2859

## Project Structure

The project submission includes the following files:

1. `proj3.tar.gz`: A compressed archive that contains all the project files.
   - `INTEGRATED-DATASET.csv`: The dataset file containing the NY Complain Data.
   - `main.py`: The main Python script that implements the Apriori algorithm.
   - `example-run.txt`: An example output of a run using the dataset.

2. `README.md`: This README file providing an overview of the project and instructions for running the program.

## Dataset

We used the **"NYPD Complaint Data Current (Year To Date)"** dataset to create the `INTEGRATED-DATASET.csv` file. This dataset contains information about crimes in different NYC boroughs, including details about the crime type, location, suspect demographics, and other attributes. Each row represents a complaint, and each column represents a different attribute for that complaint.

To narrow down the dataset for generating interesting association rules, we removed certain columns that were deemed irrelevant or sparse. Additionally, we limited the dataset to the first 3000 rows for efficiency purposes. This selection does not compromise the association rules since the dataset has no inherent order, ensuring an even distribution of observations.

The columns removed from the original dataset are as follows:
`Cmplnt_Num`, `Cmplnt_Fr_Dt`, `Cmplnt_To_Dt`, `Cmplnt_To_Tm`, `Crm_Atpt_Cptd_Cd`, `Hadevelopt`, `Ky_Cd`, `Housing_Psa`, `Jurisdiction_Code`, `Parks_Nm`, `Patrol_Boro`, `Pd_Cd`, `Station_Name`, `Transit_District`, `Vic_Age_Group`, `Vic_Race`, `Vic_Sex`, `X_Coord_Cd`, `Y_Coord_Cs`, `Latitude`, `Longitude`, `Lat_Long`, `New Georeferenced Column`.

## Running the Program

To run the program, follow these steps:

1. Ensure you have Python 3 installed on your system.

2. Navigate to the `proj3` directory.

3. Run the following command:
```
python3 main.py INTEGRATED-DATASET.csv <min_sup> <min_conf>
```

Replace `<min_sup>` with the minimum support threshold and `<min_conf>` with the minimum confidence threshold you desire for generating association rules.

For example:
```
python3 main.py INTEGRATED-DATASET.csv 0.05 0.5
```
This command will run the Apriori algorithm on the dataset file `INTEGRATED-DATASET.csv` with a minimum support of 0.05 and a minimum confidence of 0.5.

## Apriori Algorithm

We implemented the version of the Apriori algorithm described in Section 2.1.1 of Agrawal and Srikant's paper. The algorithm works as follows:

1. It starts by identifying all the frequent itemsets of length 1 in the dataset.

2. Using the frequent itemsets of length 1, it generates candidate itemsets of length k (k > 1)
