#
# GenJmeter 1.0
# Developer: BalajiVenkateswaran K
# Version: 1.0
#

import os
import sys
import json
import utils
import jmeter

# Custom Filters
include_url_having = ['api.sprig.com', '/medium.com']
exclude_url_having =['.jpeg', '.png', '.js']
exclude_methods = ['OPTIONS']

def create_jmeter_test_plan_from_har(parent_folder):

    testplan_name = utils.trim_path(parent_folder)
    jmeter_test_plan = jmeter.create_test_plan(testplan_name)

    # Iterate the sub_folders inside the parent_folder
    for folder in os.listdir(parent_folder):
        sub_folder = parent_folder + "/" + folder

        if os.path.isdir(sub_folder):
            threadgroup_name = utils.trim_path(sub_folder)
            thread_group = jmeter.create_thread_group(threadgroup_name)
            ht_thread_group = jmeter.add_thread_group(jmeter_test_plan, thread_group)

            # Iterate the HAR files insude the sub_folder
            for file in os.listdir(sub_folder):
                filename = sub_folder + "/" + file

                if os.path.isfile(filename):
                    
                    transaction_name = utils.trim_path(filename)
                    trans_controller = jmeter.create_transaction_controller(transaction_name)
                    ht_trans_controller = jmeter.add_transaction_controller(ht_thread_group, trans_controller)
                    
                    # Read the HAR file entries
                    with open(filename, 'r', encoding="utf-8") as f:
                        har_data = json.load(f)

                    # Iterate entries
                    for entry in har_data['log']['entries']:
                        request = entry['request']
                        url = request['url']
                        method = request['method']
                        bodySize = request['bodySize']
                        body = {}
                        mimeType = "text/plain"                

                        # Apply filters
                        if(utils.url_contains(url, include_url_having) and not utils.url_contains(url, exclude_url_having) and not utils.method_contains(method, exclude_methods)):
                            
                            if(bodySize > 0):                                                       
                                body = request['postData']['text']
                                mimeType = request['postData']['mimeType']                                

                            # Create and Add HTTP Sampler Request to the Transaction Controller
                            http_request = jmeter.create_http_sampler_request(utils.get_path(url), url, method, bodySize, body, mimeType)                            
                            ht_http_request = jmeter.add_http_sampler_request(ht_trans_controller, http_request)
                            # ht_http_request can be used if case of adding child items like http_request_manager

    return jmeter_test_plan          

def main():
    arguments = sys.argv[1:]
    parent_folder = arguments[0]

    # Create jmeter test plan
    jmeter_test_plan = create_jmeter_test_plan_from_har(parent_folder)

    # Save Jmeter Test Plan
    jmeter.save_test_plan(jmeter_test_plan, utils.trim_path(parent_folder)+".jmx")
    
if __name__ == "__main__":
    main()
