from faker import Faker
import pandas as pd
import random
import numpy as np

def generate_data(records_per_country):
    fake = Faker()
    Faker.seed(0)  # For reproducibility
    np.random.seed(0)  # For reproducibility

    # Note1 combinations
    task_combinations = [
        ("CA", "AAAA"), ("CA", "LMU-SP Release"), ("CA", "LMU-Legal Bills"), 
        ("CA", "LMU-CRIS"), ("CA", "LMU-Provision"), ("CA", "Settlement"),
        ("CE", "Additional Information Required"), ("CH", "BIB Maintenance Online request"),
        ("CM", "Change of address"), ("CM", "Change of Company Name"),
        # Add the rest of the combinations from Note1...
    ]
    country_codes = ["hk", "sg", "my", "uk"]

    # Table 1: CL365_UserAvailability
    user_availability = []
    for _ in range(records_per_country * len(country_codes)):
        first_name = fake.first_name().lower()
        last_name = fake.last_name().lower()
        domain = random.choice(country_codes)
        login_email = f"{first_name}.{last_name}@hsbc.com.{domain}"
        user_availability.append({
            "Login Email": login_email,
            "Available": True  # Temporarily set to True; will be updated later
        })

    user_availability_df = pd.DataFrame(user_availability)

    # Table 2: CL365_UserAvailabilityLogs
    actions = ["Log in", "Error", "Continued Case Assignment", "Log Out", 
               "Points Earned", "Stopped Case Assignment", "Task Assigned", 
               "Task Cancelled", "Task Completed", "Task Opened", "Task Returned to RM"]
    user_availability_logs = []
    
    for email in user_availability_df["Login Email"]:
        action = random.choice(actions)  # Assign a single action to the user
        task_id = None
        if action in ["Error", "Continued Case Assignment", "Points Earned", 
                      "Task Assigned", "Task Cancelled", "Task Completed", 
                      "Task Opened", "Task Returned to RM"]:
            task_id = f"TASK-{random.randint(10000, 999999)}"  # Assign task ID if applicable
        user_availability_logs.append({
            "Login Email": email,
            "Action": action,
            "TaskID": task_id
        })

    user_availability_logs_df = pd.DataFrame(user_availability_logs)

    # Update Table 1: Set Available to False if no TaskID exists in Table 2 for the same email
    def check_availability(email):
        log_entries = user_availability_logs_df[user_availability_logs_df["Login Email"] == email]
        has_task_id = log_entries["TaskID"].notna().any()
        return has_task_id  # True if TaskID exists, else False

    user_availability_df["Available"] = user_availability_df["Login Email"].apply(check_availability)

    # Table 3: CL365_UserSkillset
    user_skillset = []
    for email in user_availability_df["Login Email"]:
        for _ in range(random.randint(1, len(task_combinations))):
            task_type, sub_task = random.choice(task_combinations)
            country_code = email.split('.')[-1]
            mean_completion = int(np.random.normal(1300, 200))  # Mean ~1300, StdDev ~200
            mean_completion = max(0, min(mean_completion, 2000))
            error_rate = round(np.random.normal(0.3, 0.1), 2)  # Mean ~0.3, StdDev ~0.1
            error_rate = max(0.0, min(error_rate, 1.0))
            user_skillset.append({
                "Login Email": email,
                "TaskType": task_type,
                "Sub Task": sub_task,
                "Country Code": country_code,
                "Mean Completion": mean_completion,
                "Error Rate": error_rate
            })

    user_skillset_df = pd.DataFrame(user_skillset)

    # Table 4: CL365_TaskStatistics
    task_statistics = []
    for task_type, sub_task in task_combinations:
        for country_code in country_codes:
            task_statistics.append({
                "TaskType": task_type,
                "Sub Task": sub_task,
                "Country Code": country_code,
                "Mean Completion": None,  # Placeholder for aggregation
                "Error Rate": None       # Placeholder for aggregation
            })

    task_statistics_df = pd.DataFrame(task_statistics)

    return user_availability_df, user_availability_logs_df, user_skillset_df, task_statistics_df


# Usage Example
records_per_country = 10
table_1, table_2, table_3, table_4 = generate_data(records_per_country)

print("Table 1: User Availability")
print(table_1.head(20))
print("\nTable 2: User Availability Logs")
print(table_2.head(20))
print("\nTable 3: User Skillset")
print(table_3.head(20))
print("\nTable 4: Task Statistics")
print(table_4.head(20))
