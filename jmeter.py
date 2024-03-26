#
# Jmeter Script Generating Functions
# Developer: BalajiVenkateswaran K
# Version: 1.0
#

import xml.etree.ElementTree as ET
import utils
from urllib.parse import urlparse

def save_test_plan(test_plan, filename):
    tree = ET.ElementTree(test_plan)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print("test plan saved successfully!")

def create_test_plan(name):
    jmeter_test_plan = ET.Element("jmeterTestPlan", version="1.2", properties="5.0", jmeter="5.5")
    
    ht_test_plan = ET.Element("hashTree")
    test_plan = ET.Element("TestPlan", guiclass="TestPlanGui", testclass="TestPlan", testname=name, enabled="true")
    ET.SubElement(test_plan, "stringProp", name="TestPlan.comments")
    ET.SubElement(test_plan, "boolProp", name="TestPlan.functional_mode").text = "false"
    ET.SubElement(test_plan, "boolProp", name="TestPlan.tearDown_on_shutdown").text = "true"
    ET.SubElement(test_plan, "boolProp", name="TestPlan.serialize_threadgroups").text = "false"
    ET.SubElement(test_plan, "elementProp", name="TestPlan.user_defined_variables", elementType="Arguments", guiclass="ArgumentsPanel", testclass="Arguments", testname="User Defined Variables", enabled="true")
    element_prop = test_plan.find("./elementProp[@name='TestPlan.user_defined_variables']")
    ET.SubElement(element_prop, "collectionProp", name="Arguments.arguments")
    ET.SubElement(test_plan, "stringProp", name="TestPlan.user_define_classpath")
    
    ht_thread_group = ET.Element("hashTree")

    ht_test_plan.append(test_plan)
    ht_test_plan.append(ht_thread_group)
    jmeter_test_plan.append(ht_test_plan)    

    return jmeter_test_plan

def create_thread_group(name):

    thread_group = ET.Element("ThreadGroup", guiclass="ThreadGroupGui", testclass="ThreadGroup", testname=name, enabled="true")
    ET.SubElement(thread_group, "stringProp", name="ThreadGroup.on_sample_error").text = "continue"
    ET.SubElement(thread_group, "elementProp", name="ThreadGroup.main_controller", elementType="LoopController", guiclass="LoopControlPanel", testclass="LoopController", testname="Loop Controller", enabled="true")
    loop_controller = thread_group.find("./elementProp[@name='ThreadGroup.main_controller']")
    ET.SubElement(loop_controller, "boolProp", name="LoopController.continue_forever").text = "false"
    ET.SubElement(loop_controller, "intProp", name="LoopController.loops").text = "1"
    ET.SubElement(thread_group, "stringProp", name="ThreadGroup.num_threads").text = "10"
    ET.SubElement(thread_group, "stringProp", name="ThreadGroup.ramp_time").text = "1"    
    ET.SubElement(thread_group, "boolProp", name="ThreadGroup.scheduler").text = "false"
    ET.SubElement(thread_group, "stringProp", name="ThreadGroup.duration").text = ""
    ET.SubElement(thread_group, "stringProp", name="ThreadGroup.delay").text = ""
    ET.SubElement(thread_group, "boolProp", name="ThreadGroup.same_user_on_next_iteration").text = "true"

    return thread_group

def create_transaction_controller(name):

    trans_controller = ET.Element("TransactionController", guiclass="TransactionControllerGui", testclass="TransactionController", testname=name, enabled="true")
    ET.SubElement(trans_controller, "boolProp", name="TransactionController.includeTimers").text = "false"
    ET.SubElement(trans_controller, "boolProp", name="TransactionController.parent").text = "false"

    return trans_controller

def create_http_sampler_request(name, url, method, body_size, body, mime_type):
    
    # parse the url
    parsed_url = urlparse(url)
    domain = utils.get_domain(url)
    protocol = utils.get_protocol(url)
    path = utils.get_path(url)
    port = utils.get_port(url)

    http_request = ET.Element("HTTPSamplerProxy", guiclass="HttpTestSampleGui", testclass="HTTPSamplerProxy", testname=name, enabled="true")
        
    if(body_size > 0):    
        ET.SubElement(http_request, "boolProp", name="HTTPSampler.postBodyRaw").text = "true"
        ET.SubElement(http_request, "elementProp", name="HTTPsampler.Arguments", elementType="Arguments")
        element_prop = http_request.find("./elementProp[@name='HTTPsampler.Arguments']")
        ET.SubElement(element_prop, "collectionProp", name="Arguments.arguments")
        collection_prop = element_prop.find("./collectionProp[@name='Arguments.arguments']")

        ET.SubElement(collection_prop, "elementProp", name="", elementType="HTTPArgument")
        collection_prop_element_prop = collection_prop.find("./elementProp[@elementType='HTTPArgument']")

        ET.SubElement(collection_prop_element_prop, "boolProp", name="HTTPArgument.always_encode").text = "false"
        ET.SubElement(collection_prop_element_prop, "stringProp", name="Argument.value").text = body
        ET.SubElement(collection_prop_element_prop, "stringProp", name="Argument.metadata").text = "="
    
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.domain").text = domain 
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.port").text = port
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.protocol").text = protocol 
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.contentEncoding").text = ""
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.path").text = path
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.method").text = method
    ET.SubElement(http_request, "boolProp", name="HTTPSampler.follow_redirects").text = "true"
    ET.SubElement(http_request, "boolProp", name="HTTPSampler.auto_redirects").text = "false"
    ET.SubElement(http_request, "boolProp", name="HTTPSampler.use_keepalive").text = "true"
    ET.SubElement(http_request, "boolProp", name="HTTPSampler.DO_MULTIPART_POST").text = "false"
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.embedded_url_re").text = ""
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.connect_timeout").text = ""
    ET.SubElement(http_request, "stringProp", name="HTTPSampler.response_timeout").text = ""

    return http_request

def add_thread_group(jmeter_test_plan, thread_group):
    ht_test_plan = jmeter_test_plan.find("./hashTree")
    ht_thread_group = ht_test_plan.find("./hashTree")
    ht_thread_group.append(thread_group)

    ht_trans_controller = ET.Element("hashTree")
    ht_thread_group.append(ht_trans_controller)
    return ht_trans_controller

def add_transaction_controller(ht_parent, trans_controller):
        
    ht_parent.append(trans_controller)
    ht_child = ET.Element("hashTree")
    ht_parent.append(ht_child) # To add http sampler requests under this transaction controller
    return ht_child

def add_http_sampler_request(ht_parent, http_request):
    
    ht_parent.append(http_request)
    ht_child = ET.Element("hashTree")
    ht_parent.append(ht_child) # To add http request defauts if any
    return ht_child
