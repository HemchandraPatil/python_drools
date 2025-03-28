from python_drools_sdk.commands.insert_elements_command import InsertElementsCommand
from python_drools_sdk.commands.insert_object_command import InsertObjectCommand
from python_drools_sdk.kie.drools import Drools
from python_drools_sdk.utils import helpers
from python_drools_sdk.exceptions.drools_exception import DroolsException

# A dataclass for the example
class Person:
    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get('name', 'Papi')
        self.age = kwargs.get('age', 46)
        self.id = kwargs.get('id', None)
        self.isMajor = kwargs.get('isMajor', None)

    def __str__(self) -> str:
        return 'Person [id => {}, name => {}, age => {}, isMajor => {}]'.format(self.id, self.name, self.age, self.isMajor)

# Set configuration variables like your KIE_SERVER credentials, ROOT KIE_SERVER URL and so on
Drools.KIE_SERVER_CONTAINER_PACKAGE = 'you_kie_container_package' # Example: com.myspace.sample_project
Drools.KIE_SERVER_USERNAME = 'your_kie_server_username'
Drools.KIE_SERVER_PASSWORD = 'your_kie_server_password'
Drools.KIE_SERVER_ROOT_URL = 'https://opt/jboss/wildfly/bin/standalone.sh'
Drools.KIE_SERVER_CONTAINER_ID = 'aa1221d57ebf' # Example : Sample_Project_1.0.0-SNAPSHOT
# If you defined a KIE_SESSION in your drools workbench project, you can specify it like the following line
Drools.KIE_SESSION_NAME = 'your_kie_session_name'

# Creation of data objects
person = Person(id=1)
P1 = Person(name='Fatou', id=2, age=15)
P2 = Person(name='Daba', id=3, age=17)
P3 = Person(name='Nabou', id=4, age=28)
persons = [P1, P2, P3]

# Create an InsertObjectCommand in order to fire rules on a specific object
# The 'object' parameter represent the object to sent, 'out_identifier' should be a unique key
# that is going to used for extracting the associated object after having response from drools kie server
insert_command = InsertObjectCommand(object=person, out_identifier="person_papi").initialize()

# Create an InsertElementsCommand in order to fire rules on a list of object
# The 'objects' parameter represent the list of object to sent, 'out_identifier' should be a unique key
# that is going to used for extracting the associated objects'list after having response from drools kie server
insert_elements_command = InsertElementsCommand(objects=persons, out_identifier='persons').initialize()

# Add commands before excuting them
Drools.add_command(insert_command)
Drools.add_command(insert_elements_command)

# Execute all commands
try:
    response = Drools.execute_commands()
except DroolsException as de:
    print(de)

# Getting data by using the previous 'out_identifier' key
drools_person_response = response['person_papi']

# Getting the list of persons after drools rules execution on them by using its respective key
drools_persons_list_response = response['persons']

# I also make some helpers that will allow you to convert a json (dict) to a specific object and vice versa
# Here the 'json2object' function take as a first parameter the json/dict to be converted and as a final parameter,
# the destination type (here, the 'Person' class that we defined earlier)
person_papi_object = helpers.json2object(drools_person_response, Person)
print(person_papi_object)

# A function named 'object2json' is also defined and allow you like its name says, to convert an object to json/dict
