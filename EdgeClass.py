from ontUtils import LINK_PREDICATE,LINK_SUBJECT,change_title # type: ignore

class Edge:
    def __init__(self, edge_id,source_id,target_id,relationship,source_system):
        self.edge_id = edge_id
        self.source_id = source_id
        self.target_id = target_id
        self.relationship = relationship
        self.source_system = source_system
    def __str__(self):
            return (f"Edge(edge_id={self.edge_id}, "
                    f"source_id={self.source_id}, "
                    f"target_id={self.target_id}, "
                    f"relationship={self.relationship}, "
                    f"source_system={self.source_system})")
    def generateRDF(self,collection):
        value=self.relationship
        node1=0
        node2=0
        for element in collection.nodes:
            if element.node_id==self.source_id:
                node1=element.object_id
            elif element.node_id==self.target_id:
                node2=element.object_id
        if value!="":
            return (f"<{LINK_SUBJECT+'/'+node1}> <{LINK_PREDICATE+'#'+value}> <{LINK_SUBJECT+'/'+node2}> .\n"
                    f"\t\t\t<< <{LINK_SUBJECT+'/'+node1}> <{LINK_PREDICATE+'#'+value}> <{LINK_SUBJECT+'/'+node2}> >> <{LINK_PREDICATE+'#'+"Source_System"}> \"{self.source_system}\" .")
        return
    def generateRDFWithoutLink(self,collection):
        value=self.relationship
        node1=0
        node2=0
        
        for element in collection.nodes:
            if element.node_id==self.source_id:
                node1=element.object_id
            elif element.node_id==self.target_id:
                node2=element.object_id
        if value!="":
            return (f"{node1}  {node2} {value} \n"
                    f"{node1+value+node2} source_system {self.source_system} ")
        return
    def generateOntology(self,node1,node2):
        
        return (f"{node1.configuration_item} {node2.configuration_item} {self.relationship} ")
