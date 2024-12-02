
#We're trying to create a dataset consisting of all patients registered at GP practices in England on 31 december 2023
    #Including their age, sex, region, and if they were diagnosed with COVID in the past year (captured via test results & snomed codes)
    #tables.tpp --> patients --> has patients' age & sex
    #           --> practice_registrations --> date pt joined practice, date pt left, practice region
    #           --> sgss_covid_all_tests --> results of COVID-19 tests
    #           --> clinical_events --> the snomed code & date for each clinical event    --> NEXT STEP
    #snomed code list --> ???                                                             --> NEXT STEP


#This is telling python that we want to import a specific section of code: create_dataset from the module: ehrql
    #Module: A a file containing python code (i.e. simialr to a .do file). Modules typically have a .py extension
    #To utilise what's contained in the module (i.e. similar to a program/package in STATA), you have to import it
    #The "from" statement allows you to import a specific section of code from the module


from ehrql import create_dataset
from ehrql.tables.tpp import patients, practice_registrations

#Using the function "create_dataset" to define a dataset called "dataset_a"
#Note: You also have to define the population of the dataset using the function "define_population"
    #It's generally easier to define the conditions first, then include the pre-defined conditions in the "define_population" function

dataset = create_dataset()
reg_date = "2023-12-31"

dataset.define_population(practice_registrations.for_patient_on(reg_date).exists_for_patient())
    #for_patient_on: returns each patient's practice registration status for the supplied date
    #exists_for_patient: Makes sure the dataframe only contains patients where the previously specified condition = True 
    #So, the code is saying: For each patient that is registered on "reg_date", only include them if the condition = True 

# SYNTAX NOTES:
# Including other characteristics to define the population by:
    #E.g. We now want everyone who was registered on December 31 2023, and whose practice is located in the West Midlands
    # dataset.define_population((practice_registrations.for_patient_on(reg_date).exists_for_patient()) & (practice_registrations.for_patient_on(reg_date).practice_nuts1_region_name.is_in(["West Midlands"]))
    #"for_patient_on(reg_date)" is repeated because each condition has to have the same "level" of filtering
        #"for_patient_on(reg_date)" --> returns the patient's registration status on reg_date
        #"practice_nuts1_region_name.is_in(["West Midlands"])" --> specifies that the practice region is in the west midlands
    #If you don't specify the same "level of filtration" in the second part of the code, ehrQl will try to merge all patients registered on reg_date with all patients at practices located in the West Midlands
        #ehrQL will try to do a many:1 merge of patient data and it can't handle that

    #It's easier to read & debug your code if you define your characteristics first, separately:
        #reg_date "2023-12-31"
        #has_registration = practice_registrations.for_patient_on(reg_date).exists_for_patient() 
        #in_region = practice_registrations.for_patient_on(reg_date).practice_nuts1_region_name.is_in(["West Midlands", "London"])
            #dataset.define_population(has_registration & in_region)

#dataset.sex = patients.sex
#dataset.age = patients.age_on(index_date)
#dataset.age_plus1 = patients.age_on(index_date)+1
#dataset.age_plus2 = patients.age_on(index_date)+2