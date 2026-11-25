
import client_config

print("\nSearch Keywords:")
for keyword in client_config.SEARCH_KEYWORDS:
    print("-", keyword)

print("\nLocation:", client_config.LOCATION)
print("Post Age:", client_config.POST_AGE_HOURS, "hours")
print("Data Directory:", client_config.DATA_DIR)
