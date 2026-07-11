import requests

def resolve_radio(radio: str) -> int:
    """
    Resolve the MMSI of a vessel based on its radio callsign, and return the MMSI
    """
    url = f"https://kystdatahuset.no/ws/api/ship/combined/callsign/{radio}"

    headersList = {
 "User-Agent": "Your Client (https://your-client.com)",
 "Content-Type": "application/json",
 "Authorization": "Bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwidHlwIjoiSldUIiwiY3R5IjoiSldUIn0..kNjKZCKrfZVDc6G6yQiwdw.j8I3jN21w7MTApM1xEVcNT8k6D-KamZ1oqWIyArAh0MePMX9O8x7K2l625Roqp78wusYcLnMCu3qLKCRUEsLJYoiCRWYqDjnZpR1meKmFnFFq069L61r4uGHfogzaXwOWmH3u7aLaPsaJ11MqqIExGDxnS-Onl_x_wHtISGjKaBpRY0Harm1a8V-oyA911kOM0HOhG2U7nB4xOFI-yNfwwKmI1glHHMuv558yNj2eIzvER4noJwWqipc_e9FYSegZUhM5VmdLGaGnNaw4S3rsOKguKyLv1wsS-p0fA3VeLmQRaairzQY1BSx7bv8hvM_DmvvnuNct5PcyLGefgkfLItG6f6RMWQBNdegLFbZHmazDwyE0v-1Q3Q3y9HqLGoDrRySzkBm8u9z57DL5VAYp7pzIMHgX8UO4SgyJPLMBhYSeGdzRpHu8kABiSJv_-IMhgF7W8vGWhattj6JAi3_cxnrIx8eJNu91uV05zJAGH8fZWIYg-HmRdNTxaaPGIkaeyH-z3XKO-QWiIQevVYr_rWy6pwNkoC1eOg92qxcNIjkyxFc1jlb-y-eYIUM-2GIIUqISHCpx_S82IKx1jjnrviSUJSuxV8nyJot_mHEpVzd52-YhVHN40nPPAKL2VhZORO6MkvIj-M5HQBiywfMWg.l1u5qWMnjEyi_DdP_6WAe3LxOc8bsnW0Su29l7oK0Zo"
}


    r = requests.get(url, headers=headersList)
    if r.status_code != 200:
        print(f"[!] Could not resolve mmsi from radio ({radio})")
        print(r.status_code)
        print(r.text)
        return None
    try:
        res = r.json()
    except:
        print("[!] Could not parse JSON response body")
        print(r.text)
        return None

    if not res.get("success") == True or res.get("data") == None:
        print(f"[!] Error in response to resolve mmsi from radio ({radio})")
        print(r.text)
        return None

    # If multiple entries returned, get the non-zero MMSI
    for msg in res.get("data"):
        if msg.get("mmsi", 0) <= 0:
            continue
        return msg.get("mmsi")