3. api-service/ 🌐
Frontend interface.

Receives API calls from the frontend:

GET /donor-search?blood=A+&location=...

POST /donor-registration

Forwards requests to search-service, auth-service, or others as needed.

✅ Single entry point for the client (React, mobile, etc.).


### **1. The API Endpoint**

Think of this as the front door. When someone needs to find a donor, they "knock" on this door with the following details:

- **Blood type** needed (e.g., `"A+"`, `"O-"`)
- **Location** (ZIP code)
- **Distance** they're willing to travel
- **Urgency** of the request

The API handles:

- Secure **database connections**
- Data **validation and formatting**
- Efficient **querying and scoring**
- Smooth and fast **response delivery**



