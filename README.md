# genjmeter version 1.0

genjmeter helps to generate the jmeter test plan (script) from the organized HAR files.
The HAR files must be captured separately for each step in the user navigation and named appropriately. For example, 01_myportal_home.har, 02_myportal_login.har, 03_click_search.har etc., These files must be organized inside a sub-folder / directory with appropriate name for that user journey. The sample organization of HAR files in the folder structure is given below:

    myportal (folder) / (test plan)
    |
    |__ products_search  (sub-folder) / (user journey) / (threadgroup)
        |
        |__01_products_search_myportal_home.har (transaction controller)
        |
        |__02_products_search_myportal_login.har (transaction controller)
        |
        |__03_products_search_click_search.har (transaction controller)

# Applicaton usage:

Goto to the parent folder containing the genjmeter. Run the command,

$ python ./genjmeter ./myportal
