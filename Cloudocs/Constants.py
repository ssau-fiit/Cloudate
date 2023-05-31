class ServerAPI:
    url = "http://10.60.7.203:8080"
    host = "10.60.7.203"
    port = "8080"
    # POST
    auth = "/api/v1/auth"
    createDocument = "/api/v1/documents/create"

    # GET
    getDocuments = "/api/v1/documents"
    getDocument = "/api/v1/documents/"  # get by ID, post by ID (change text), delete by ID


class OpType:
    INSERT = "INSERT"
    DELETE = "DELETE"
