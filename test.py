###
# Fichier de tests de tout et n'importe quoi
###

# For windows the path will look like
#    a. exp_path="complete\\path\\to\\NTU_Experiment"
# or b. exp_path=r"complete\path\to\NTU_Experiment"
from PyTrack.Experiment import Experiment
from PyTrack.formatBridge import generateCompatibleFormat

# Sebastien : exp_path="C:/Users/Sebastien/PycharmProjects/PII/NTU_Experiment"

generateCompatibleFormat(exp_path="F:/PII/NTU_Experiment",
                         device="eyelink",
                         stim_list_mode='NA',
                         eye='B',
                         reading_method="CSV")


print("1 is OK")

# Creating an object of the Experiment class
exp = Experiment(json_file="F:/PII/NTU_Experiment/NTU_Experiment.json",
                 csv_path="F:/PII/NTU_Experiment/Data/csv_files",
                 reading_method="CSV")

print("2 is OK")

# Instantiate the meta_matrix_dict of an Experiment to find and extract all features from the raw data
exp.metaMatrixInitialisation()

print("3 is OK")

# Calling the function for the statistical analysis of the data
exp.analyse(parameter_list={"all"},
            between_factor_list=["Subject_type"],
            within_factor_list=["Stimuli_type"],
            statistical_test="anova",
            file_creation=True)

print("4 is OK")

# Does not run any statistical test. Just saves all the data as csv files.
exp.analyse(parameter_list={"all"},
            statistical_test="None",
            file_creation=True)

print("5 is OK")

# This function call will open up a GUI which you can use to navigate the entire visualization process
exp.visualizeData()

print("6 is OK")
