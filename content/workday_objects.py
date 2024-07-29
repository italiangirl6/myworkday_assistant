
class WorkdayDOMObjects():
    # Login Page
    login_username = "//label[contains(., 'Email')]/..//input"
    login_password = "//label[contains(., 'Password')]/..//input"
    login_submit = "//label[contains(., 'Password')]/../../..//button"

    # Dashboard
    jobs_active_label = "//button[contains(., 'Active')]"
    you_have_no_label = "//p[contains(., 'You have no applications.')]"
    my_applications_label = "//h3[contains(.,'My Applications')]"
    table_rows = "//table/tbody/tr"
    one_entry_title = "//table/tbody/tr/th//a"
    one_entry_status = "//table/tbody/tr/td/div//span"
    one_entry_submit_date = "//table/tbody/tr/td[3]"