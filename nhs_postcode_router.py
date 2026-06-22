import re

import httpx

# Official NHS Digital ODS ORD API Endpoint
NHS_ODS_BASE_URL = "https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations"


def clean_and_validate_postcode(postcode: str) -> str | None:
    """Sanitises input and validates against a standard UK postcode regex."""
    cleaned = re.sub(r"\s+", "", postcode).upper()
    pattern = r"^[A-Z]{1,2}[0-9][A-Z0-9]??[0-9][A-Z]{2}$"
    return cleaned if re.match(pattern, cleaned) else None


def fetch_postcode_data(postcode: str) -> dict | None:
    """Fetches geographic and administrative codes from Postcodes.io."""
    url = f"https://api.postcodes.io/postcodes/{postcode}"
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            return response.json().get("result", {})
    except httpx.RequestError:
        print("\n[Error] Unable to connect to Postcodes.io.")
    return None


def fetch_nhs_ods_record(ods_code: str) -> dict | None:
    """Queries the official NHS Digital ODS API for an organisation's
    full live record."""
    url = f"{NHS_ODS_BASE_URL}/{ods_code}"
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            return response.json().get("Organisation", {})
    except httpx.RequestError:
        print(f"\n[Error] Failed to connect to NHS ODS API for code {ods_code}.")
    return None


def display_routing_summary(api_data: dict) -> None:
    """Combines both API datasets to present live administrative routing."""
    print("\n" + "=" * 55)
    print(f" 📑 LIVE NHS DATA ROUTING FOR: {api_data.get('postcode')}")
    print("=" * 55)

    print("\n📍 GEOGRAPHY")
    print(f"  Region:       {api_data.get('region', 'Unknown')}")
    print(f"  Country:      {api_data.get('country', 'Unknown')}")
    print(f"  Constituency: {api_data.get('parliamentary_constituency', 'Unknown')}")

    print("\n🏢 NHS ADMINISTRATIVE BOUNDARY")

    icb_ods_code = api_data.get("codes", {}).get("ccg_id")
    ons_code = api_data.get("codes", {}).get("ccg", "Unknown")

    if not icb_ods_code:
        print("  Integrated Care Board (ICB): No valid ODS boundary resolved.")
    else:
        print(f"  Fetching official profile for ODS Code: '{icb_ods_code}'...")
        ods_record = fetch_nhs_ods_record(icb_ods_code)

        if ods_record:
            official_name = ods_record.get("Name", "Unknown")
            status = ods_record.get("Status", "Unknown")

            # Extract main address components if available
            address = ods_record.get("GeoLoc", {}).get("Location", {})
            town = address.get("Town", "Unknown Location")
            post_code = address.get("PostCode", "")

            print("\n  ✅ Live Match Resolved via National Spine:")
            print(f"  Official Name:    {official_name}")
            print(f"  Operational ODS:  {icb_ods_code}")
            print(f"  Spine Status:     {status}")
            print(f"  HQ Location:      {town} ({post_code})")
            print(f"  ONS Area Code:    {ons_code}")
        else:
            print(f"  Allocated ICB Name: {api_data.get('ccg', 'Unknown')}")
            print(f"  ODS Code:           {icb_ods_code}")

    print("\n" + "=" * 55 + "\n")


def main() -> None:
    print("NHS Postcode & Live ODS Core Router Initialised (100% Dynamic).")
    print("Type 'exit' or 'quit' to safely terminate.")

    while True:
        user_input = input("Enter patient postcode: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Shutting down routing utility. Goodbye!")
            break

        if not user_input:
            continue

        validated_postcode = clean_and_validate_postcode(user_input)
        if not validated_postcode:
            print("❌ Invalid UK postcode format (e.g., TA12 6JL).\n")
            continue

        print("🔄 Resolving postcode coordinates...")
        api_data = fetch_postcode_data(validated_postcode)

        if api_data:
            display_routing_summary(api_data)
        else:
            print("❌ Postcode not found in the national directory.\n")


if __name__ == "__main__":
    main()
