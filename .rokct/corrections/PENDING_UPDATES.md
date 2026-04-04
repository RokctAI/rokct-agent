# Pending Post-Bake Configuration

The following items must be updated after the codebase is baked into the production environment:

1.  **Frappe Schema Path**: 
    Update `SCHEMA_PATH` in `tools/frappe_dynamic.py` to point to the actual tenant site path.
    Currently defaults to: `/home/frappe/frappe-bench/apps/rcore/rcore/platform/schemas/ai_tools.json`

2.  **Environment Variables**:
    Ensure the following are set in the tenant's `.env`:
    - `FRAPPE_BASE_URL`
    - `FRAPPE_API_KEY`
    - `FRAPPE_API_SECRET`
    - `WHATSAPP_ALLOWED_USERS`

3.  **Role Verification**:
    The agent uses `get_rokct_app_role()` to determine if it should use the `control` or `tenant` API gateway. Ensure the site configuration matches the expected role.
