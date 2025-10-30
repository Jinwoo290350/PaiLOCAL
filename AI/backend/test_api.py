"""Test script for Plan My Trip API"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_themes():
    """Test get themes endpoint"""
    print("\n=== Testing GET /api/themes ===")
    response = requests.get(f"{BASE_URL}/api/themes")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Number of themes: {len(data['themes'])}")
    for theme in data['themes']:
        print(f"  - {theme['id']}: {theme['name']} ({theme['icon']})")


def test_search_places():
    """Test search places endpoint"""
    print("\n=== Testing GET /api/places/search ===")

    # Test 1: Simple search
    print("\n1. Search for 'ภู':")
    response = requests.get(
        f"{BASE_URL}/api/places/search",
        params={"query": "ภู", "limit": 3}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data['results'])} places:")
    for place in data['results']:
        print(f"  - {place['name']} ({place['keyword']})")

    # Test 2: Search with distance calculation
    print("\n2. Search for 'วัด' with distance:")
    response = requests.get(
        f"{BASE_URL}/api/places/search",
        params={
            "query": "วัด",
            "limit": 3,
            "start_lat": 19.9105,
            "start_lng": 99.8406
        }
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data['results'])} places:")
    for place in data['results']:
        print(f"  - {place['name']} - {place['distance_km']} km")


def test_plan_trip_theme():
    """Test plan trip with theme mode"""
    print("\n=== Testing POST /api/plan-trip (Theme Mode) ===")

    request_data = {
        "start_lat": 19.9105,
        "start_lng": 99.8406,
        "mode": "theme",
        "value": "naturalist",
        "num_stops": 5,
        "max_distance_km": 50
    }

    print(f"\nRequest: {json.dumps(request_data, indent=2)}")

    response = requests.post(
        f"{BASE_URL}/api/plan-trip",
        json=request_data
    )

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n=== Trip Summary ===")
        print(f"Trip ID: {data['trip_id']}")
        print(f"Mode: {data['mode']}")
        print(f"Theme: {data.get('theme', 'N/A')}")
        print(f"\nSummary:")
        print(f"  Total Stops: {data['summary']['total_stops']}")
        print(f"  Total Distance: {data['summary']['total_distance_km']} km")
        print(f"  Estimated Time: {data['summary']['estimated_time_hours']} hours")
        print(f"  Total Carbon: {data['summary']['total_carbon_kg']} kg CO2")
        print(f"  Eco Score: {data['summary']['eco_score']}/10")
        print(f"  Carbon Reduction: {data['summary']['carbon_reduction_percent']}%")

        print(f"\n=== Route ===")
        for place in data['route']:
            print(f"\nStop {place['stop_number']}: {place['name']}")
            print(f"  Keyword: {place['keyword']}")
            print(f"  Rating: {place['rating']} ({place['user_ratings_total']} reviews)")
            print(f"  Distance from prev: {place['distance_from_prev_km']} km")
            print(f"  Carbon: {place['carbon_kg']} kg CO2")
            print(f"  Photos: {len(place['photos'])} photo(s)")
    else:
        print(f"Error: {response.text}")


def test_plan_trip_place_name():
    """Test plan trip with place_name mode"""
    print("\n=== Testing POST /api/plan-trip (Place Name Mode) ===")

    request_data = {
        "start_lat": 19.9105,
        "start_lng": 99.8406,
        "mode": "place_name",
        "value": "ฟาร์ม",
        "num_stops": 4,
        "max_distance_km": 30
    }

    print(f"\nRequest: {json.dumps(request_data, indent=2)}")

    response = requests.post(
        f"{BASE_URL}/api/plan-trip",
        json=request_data
    )

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\n=== Trip Summary ===")
        print(f"Trip ID: {data['trip_id']}")
        print(f"Mode: {data['mode']}")
        print(f"Based on place: {data.get('place_name', 'N/A')}")
        print(f"\nTotal Stops: {data['summary']['total_stops']}")
        print(f"Total Carbon: {data['summary']['total_carbon_kg']} kg CO2")
        print(f"Eco Score: {data['summary']['eco_score']}/10")

        print(f"\n=== Route ===")
        for place in data['route']:
            print(f"Stop {place['stop_number']}: {place['name']} ({place['keyword']})")
    else:
        print(f"Error: {response.text}")


if __name__ == "__main__":
    print("=" * 60)
    print("Plan My Trip API - Test Suite")
    print("=" * 60)

    try:
        # Run all tests
        test_health()
        test_get_themes()
        test_search_places()
        test_plan_trip_theme()
        test_plan_trip_place_name()

        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server!")
        print("Please make sure the server is running:")
        print("  cd backend && python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
