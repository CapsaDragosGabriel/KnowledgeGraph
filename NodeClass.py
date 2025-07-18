# NodeClass.py
from ontUtils import LINK_PREDICATE,LINK_SUBJECT,change_title # type: ignore

class Node:
    def __init__(self, node_id, object_id,object_name,configuration_item,source_system,model_type):
        self.node_id = node_id
        self.object_id = object_id
        self.object_name = object_name
        self.configuration_item = configuration_item
        self.source_system = source_system
        self.model_type = model_type
    def __str__(self):
        return (f"Node(node_id={self.node_id}, "
                f"object_id={self.object_id}, "
                f"object_name={self.object_name}"
                f"configuration_item={self.configuration_item}, "
                f"source_system={self.source_system}, "
                f"model_type={self.model_type})")
    def generateRDF(self,property):
        value=getattr(self,property)
        if value!="":
            if property=="object_name" or property=="model_type" or property=="source_system":
                value=value.replace("\"","")
                if property=="object_name":
                    property="Label"
                return (f"<{LINK_SUBJECT+'/'+self.object_id}> <{LINK_SUBJECT+'#'+change_title(property)}> \"{value}\" .")
            elif property=="configuration_item":
                return (f"<{LINK_SUBJECT+'/'+self.object_id}> <{LINK_SUBJECT+'#'+change_title(property)}> <{LINK_SUBJECT+'#'+value}> .")
            else:
                return (f"<{LINK_SUBJECT+'/'+self.object_id}> <{LINK_SUBJECT+'#'+change_title(property)}> <{LINK_SUBJECT+'/'+value}> .")
                
        return ""
    
    def generateRDFWithoutLink(self,property):
        value=getattr(self,property)
        value=value.replace(" ","-")
        if value!="":
            return (f"{self.object_id} {value} {property} ")
                
        return ""
    
    def generateOntology(self,property):
        value=getattr(self,property)
        value=value.replace(" ","-")
        print(self)
        print(property)
        if value!="":
            if property=="source_system":
                return (f"{self.configuration_item} {"Source_System"} {"definedIn"} ")
            if property=="model_type":
                return (f"{self.configuration_item} {"Model_Type"} {"hasModel"} ")
        return
               
        