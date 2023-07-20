import plantuml

def generate_sequence_diagram():
    diagram_code = """
    @startuml
    participant User
    participant IDM
    participant AuthenticationProvider

    User -> IDM: Send authentication request
    IDM -> AuthenticationProvider: Forward request
    AuthenticationProvider -> IDM: Return authentication result
    IDM -> User: Return authentication result

    @enduml
    """

    # Generate the diagram and save it as an image
    plantuml.PlantUML().processes_bytes(diagram_code.encode('utf-8')).write("authentication_sequence_diagram.png")

if __name__ == "__main__":
    generate_sequence_diagram()