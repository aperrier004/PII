from PyTrack.formatBridge import generateCompatibleFormat
from PyTrack.Experiment import Experiment


# For windows the path will look like
#    a. exp_path="complete\\path\\to\\NTU_Experiment"
# or b. exp_path=r"complete\path\to\NTU_Experiment"
generateCompatibleFormat(exp_path="F:/PII/NTU_Experiment",
                         device="eyelink",
                         stim_list_mode='NA',
                         start='start_trial',
                         stop='stop_trial',
                         eye='B')

# Creating an object of the Experiment class
exp = Experiment(json_file="F:/PII/NTU_Experiment/NTU_Experiment.json")


# Instantiate the meta_matrix_dict of an Experiment to find and extract all features from the raw data
exp.metaMatrixInitialisation()

# Calling the function for the statistical analysis of the data
exp.analyse(parameter_list={"all"},
            between_factor_list=["Subject_type"],
            within_factor_list=["Stimuli_type"],
            statistical_test="anova",
            file_creation=True)

# Does not run any statistical test. Just saves all the data as csv files.
exp.analyse(parameter_list={"all"},
            statistical_test="None",
            file_creation=True)


# This function call will open up a GUI which you can use to navigate the entire visualization process
exp.visualizeData()
