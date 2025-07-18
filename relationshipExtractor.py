from NodeClass import Node # type: ignore
from EdgeClass import Edge # type: ignore
from graphviz import Digraph

DESIRED_PATH="D:\\Knowledge Graph\\Migration\\"

def csv_to_edge(csv_string):
    
    #might need to include quotation (') in property  
    arrayParams=[item.strip(" '") for item in csv_string.split(',')]
    edge = Edge(
        edge_id=arrayParams[0],
        source_id=arrayParams[1],
        target_id=arrayParams[2],
        relationship=arrayParams[3],
        source_system=arrayParams[4]
    )
    
    return edge
    
def csv_to_node(csv_string):
    
    #might need to include quotation (') in property  

    arrayParams=[item.strip(" '") for item in csv_string.split(',')]
   
    
    node = Node(
        node_id=arrayParams[0],
        object_id=arrayParams[1],
        object_name=f"\"{arrayParams[2]}\"",
        configuration_item=arrayParams[3].replace(" ","_"),
        source_system=arrayParams[4].replace(" ","_"),
        model_type=arrayParams[5].replace(" ","_")
    )
    
    return  node
       
class Collection:
    nodes=[]
    edges=[]
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
    
    def getNodeById(self,node_id):
        for item in self.nodes:
            if item.node_id==node_id:
                return item
        return
    def getNodesObjectIds(self):
        arr=[]
        for item in self.nodes:
            arr.append(item.object_id)
        return arr
    def replaceDuplicateRelationships(self):
        for item in self.edges:
            src=self.getNodeById(item.source_id)
            tgt=self.getNodeById(item.target_id)
            if item.relationship=="consistsOf": 
                if src.configuration_item=="Functional_Model":
                    item.relationship="functionalDiagram"
                elif src.configuration_item=="Logical_Model":
                    item.relationship="logicalDiagram"
                elif src.configuration_item=="Physical_Model":
                    item.relationship="physicalStructure"
                elif src.configuration_item=="Physical_Structure":
                    item.relationship="hasComponent"
                elif src.configuration_item=="Component":
                    if tgt.configuration_item=="Domain":
                        item.relationship="hasDomain"
                    if tgt.configuration_item=="Component":
                        item.relationship="hasComponent"
                elif src.configuration_item=="Production_Order":
                    item.relationship="createdBy"
                if item.relationship=="consistsOf":
                    print(src)
                    print (tgt)
                    print()
            if item.relationship=="isProducedBy":
                if src.configuration_item=="Production_Order":
                    item.relationship="createdBy"
def pruneFile(filePath):
    with open(filePath, "r") as infile:
        lines = infile.readlines()
    unique_lines = list(dict.fromkeys(lines)) 
    with open(filePath, "w") as outfile:
        outfile.writelines(unique_lines)
        
def extractCollection(collection):
    with open("D:\\Knowledge Graph\\Migration\\source.txt") as f:
        l = f.readlines()
        for line in l:
            line=line.strip()
            
            search_insert="INSERT INTO \""
            if line.find(search_insert)>-1:
                start_pos=len(search_insert)
                ## getting the table name
                substr=line[start_pos:]
                get_table=substr[:substr.index("\"")].strip()
                #getting the instance values
                s=(" VALUES (")
                get_params=substr[ substr.index(s)+len(s):substr.index(");")]
                
                if(get_table=="EDGES"):
                    collection.edges.append(csv_to_edge(get_params))
                elif (get_table=="NODES"):
                    collection.nodes.append(csv_to_node(get_params))
    #first thing, generate triples out of node properties
    
#technically it is more efficient to build all the files at once, but it looks ugly, so we do it separately

def buildOntology(collection,node_properties=[],ont_file_path="",wanted_properties=[],wanted_nodes=[]):
    if ont_file_path=="":
        ont_file_path=DESIRED_PATH+"\\output\\ontology.txt"
    ont_file = open (ont_file_path,"w")
    text=[]
    #unless specified otherwise, get all nodes
    if wanted_nodes==[]:
        wanted_nodes=collection.getNodesObjectIds()
        
        
    for item in collection.nodes:
        #check if we have ani specified properties that we want from the nodes eg Source System, Model Type
        #this information is not always needed so i made it optional
        if wanted_properties!=[]:
            for property in node_properties:  
                if property in wanted_properties:
                    if (item.object_id in wanted_nodes):
                        ont=item.generateOntology(property)
                        if(ont):
                            # ont_file.write(ont+'\n')
                            text.append(ont+'\n')
    
    for item in collection.edges:
        #collect the nodes, then check if any of them is in the specified wanted nodes
        #this is for building partial ontologies, if we want to see for example how 3 out of 10 components
        #interact with each other
        node1 = collection.getNodeById(item.source_id)
        node2 = collection.getNodeById(item.target_id)
        if node1.object_id in wanted_nodes or node2.object_id in wanted_nodes:
            ont = item.generateOntology(node1,node2)
            # ont_file.write(ont+'\n')
            text.append(ont+'\n')
    ont_file.writelines(text)     
    ont_file.close()
        
    pruneFile(ont_file_path)

def buildRDFTriples(collection,node_properties=[],rdf_file=""):
    if rdf_file=="":
        rdf_file= open(DESIRED_PATH+"\\output\\generate.sql","w")
    
    rdf_file.write(f"CALL SPARQL_EXECUTE('\n"
                   "\tINSERT DATA {\n"
                   "\t\tGRAPH <iday_graph> {\n"
                   )
    for item in collection.nodes:
        for property in node_properties:  
            line=item.generateRDF(property)
            if line != "":
                rdf_file.write('\t'*3+line+'\n')
    for item in collection.edges:
        line=item.generateRDF(collection)
        # ontGraph.edge(item.source_id,item.target_id,item.relationship)
        if line != "":
            rdf_file.write('\t'*3+line+' \n')
    rdf_file.write("\t\t}\n" 
                   "\t}\', \'\', ?, ?);")
    rdf_file.close()
    
def buildInstanceGraph(collection,name=""):
    if name=="":
        name='Instances Graph'
    dot = Digraph(name)
    graph_nodes=[]
    for item in collection.nodes:
        graph_nodes.append(item.object_id)
        dot.node(item.node_id,item.object_name)
        # dot.node(item.object_id,item.object_name)
    for item in collection.edges:
        dot.edge(item.source_id,item.target_id,item.relationship)
    dot.render(directory=DESIRED_PATH+"output")
    dot.render(view=True,quiet=True)
    
def buildOntologyGraph(collection,ont_file_path="",name=""):
    if name=="":
        name='Ontology Graph'
    ontGraph=Digraph(name)
    addedNodes=[]
    if ont_file_path=="":
        ont_file_path=DESIRED_PATH+"\\output\\ontology.txt"
    with open(ont_file_path) as ont_file:
        for line in ont_file.readlines():
            # line=ont_file.readline()
            line=line.split(" ")
            addedNodes.append(line[0])
            addedNodes.append(line[1])
                                  
            ontGraph.node(line[0],line[0])
            ontGraph.node(line[1],line[1])
            ontGraph.edge(line[0],line[1],line[2])
    # add nodes that do not have a relationship with any objects
    for item in collection.nodes:
        if item.configuration_item not in addedNodes:
            addedNodes.append(item.configuration_item)
            ontGraph.node(item.object_name,item.object_name)
            

    ontGraph.render(directory=DESIRED_PATH+"output")
    ontGraph.render(view=True,quiet=True)
    
    
    

def main():
    collection= Collection([],[])
    extractCollection(collection)
    
    
    node_properties=["object_name","configuration_item","source_system","model_type"]
    
    
    # gen_file= open(os.path.join("output","generate.sql"),"w")
    # os.makedirs("output", exist_ok=True)
    collection.replaceDuplicateRelationships()#replace edges with the same name according to a (invented) naming convention
    
    
    buildRDFTriples(collection,node_properties)
    
    #node properties that we want included in the ontology
    wanted_properties=["source_system","model_type"]
    
    # wanted_nodes=["EIN200000001023","EIN204908763215","EIN20432698475"]
    buildOntology(collection,node_properties,"",[])
    
    
    # buildGraph unless told otherwise
    try:
        if buildGraphs==False:
            pass
    except NameError:
        try:
            buildInstanceGraph(collection)
            buildOntologyGraph(collection)
        except :
            pass
if __name__== "__main__":
    main()
    