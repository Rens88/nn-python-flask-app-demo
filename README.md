# Deploy a Python (Streamlit) web app to Azure App Service - Sample Application

This is a sample Streamlit application configured for Azure App Service using `azd`. The app code lives in `app.py` and renders a simple greeting UI so you can validate Streamlit deployment behavior in your Azure environment.

**Local run**
1. `python -m venv .venv`
2. `source .venv/bin/activate` (or `.\.venv\Scripts\activate` on Windows)
3. `pip install -r requirements.txt`
4. `streamlit run app.py`

**Azure App Service**
The Azure provisioning files in `infra/` set a startup command that runs Streamlit on port `8000`, which matches App Service expectations. After provisioning with `azd up`, the app should be reachable at the default App Service URL.

Sample applications are available for other frameworks here:
* Django [https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)
* FastAPI [https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).
