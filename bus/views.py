from django.http import JsonResponse
import requests
import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)

def fetch_bus_locations(request):
    service_key = "APIkey"  # 디코딩된 API 키
    route_number = request.GET.get('route_id')  # 사용자가 입력한 노선 번호

    if not route_number:
        return JsonResponse({"status": "error", "message": "No route_id provided."}, status=400)

    # 1. 노선 번호를 busRouteId로 변환
    route_url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList"
    route_params = {
        "serviceKey": service_key,
        "strSrch": route_number,
        "resultType": "json"
    }

    try:
        # 노선 번호 -> 노선 ID 변환
        route_response = requests.get(route_url, params=route_params)
        route_response.raise_for_status()
        route_data = route_response.json()

        item_list = route_data.get('ServiceResult', {}).get('msgBody', {}).get('itemList', [])
        if not item_list:
            return JsonResponse({"status": "error", "message": "Invalid bus route number."})

        # 첫 번째 결과에서 busRouteId 추출
        bus_route_id = item_list[0].get('busRouteId')

        # 2. busRouteId로 버스 위치 조회
        position_url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid"
        position_params = {
            "serviceKey": service_key,
            "busRouteId": bus_route_id,
            "resultType": "json"
        }

        position_response = requests.get(position_url, params=position_params)
        position_response.raise_for_status()
        position_data = position_response.json()

        # 버스 위치 데이터 처리
        items = position_data.get('ServiceResult', {}).get('msgBody', {}).get('itemList', [])
        if not items:
            return JsonResponse({"status": "error", "message": "No buses found for this route."})

        buses = [
            {
                "bus_id": item["vehId"],
                "latitude": float(item["tmY"]),
                "longitude": float(item["tmX"]),
                "vehicle_number": item["plainNo"]
            }
            for item in items
        ]

        return JsonResponse({"status": "success", "buses": buses})

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return JsonResponse({"status": "error", "message": f"API request failed: {str(e)}"}, status=500)
    except KeyError as e:
        logger.error(f"Missing key in response data: {e}")
        return JsonResponse({"status": "error", "message": f"Missing key: {str(e)}"}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({"status": "error", "message": f"Unexpected error: {str(e)}"}, status=500)

def map_view(request):
    # map.html 템플릿 렌더링
    return render(request, 'map.html')