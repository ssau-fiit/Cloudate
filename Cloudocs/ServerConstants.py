class Server:
    url = "http://api.cloudocs.parasource.tech:8080"

    # POST
    auth = "/api/v1/auth"
    createDocument = "/api/v1/documents/create"

    # GET
    getDocuments = "/api/v1/documents"
    getDocument = "/api/v1/documents/"  # get by ID, post by ID (change text), delete by ID