
import os
from plugins.memory import discover_memory_providers, load_memory_provider

def test_discovery():
    providers = discover_memory_providers()
    print("Discovered providers:", providers)
    
    rokct_provider = next((p for p in providers if p[0] == "rokct"), None)
    if rokct_provider:
        print("Rokct provider found!")
    else:
        print("Rokct provider NOT found.")

    # Mock environment for is_available check
    os.environ["FRAPPE_BASE_URL"] = "http://test.local"
    os.environ["FRAPPE_API_KEY"] = "key"
    os.environ["FRAPPE_API_SECRET"] = "secret"
    
    provider = load_memory_provider("rokct")
    if provider:
        print(f"Loaded provider: {provider.name}")
        print(f"Is available: {provider.is_available()}")
        print(f"Tool schemas: {provider.get_tool_schemas()}")
    else:
        print("Failed to load rokct provider.")

if __name__ == "__main__":
    test_discovery()
