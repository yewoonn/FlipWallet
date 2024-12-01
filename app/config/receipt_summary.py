def extract_receipt_summary(original_data):
    """
    OCR 오리지날 데이터에서 필요한 부분만 추출해서 요약된 내용 만드는 함수
    """
    try:
        # 이미지 리스트 확인
        images = original_data.get("images", [])
        if not images:
            return {"error": "이미지 파일이 없습니다."}  # 이미지가 없을 경우 에러 반환

        # 첫 번째 이미지에서 영수증 데이터를 추출
        receipt = images[0].get("receipt", {}).get("result", {})
        if not receipt:
            return {"error": "영수증 데이터가 없습니다."}  # 영수증 데이터가 없을 경우 에러 반환

        # 필요한 필드 추출
        store_name = receipt.get("storeInfo", {}).get("name", {}).get("text", "Unknown Store")  # 가게 이름
        payment_date = receipt.get("paymentInfo", {}).get("date", {}).get("text", "Unknown Date")  # 결제 날짜
        payment_time = receipt.get("paymentInfo", {}).get("time", {}).get("text", "Unknown Time")  # 결제 시간
        payment_card = receipt.get("paymentInfo", {}).get("cardInfo", {}).get("company", {}).get("text",
                                                                                                 "Unknown Card")  # 카드사 정보
        total_price = receipt.get("totalPrice", {}).get("price", {}).get("formatted", {}).get("value", "0")  # 총 결제 금액

        # 항목 리스트 추출
        items = []
        sub_results = receipt.get("subResults", [])
        for sub_result in sub_results:
            for item in sub_result.get("items", []):
                item_name = item.get("name", {}).get("text", "알 수 없는 item 이름")  # 항목 이름
                items.append(item_name)

        # 요약 데이터 구성 및 반환
        summary = {
            "store_name": store_name,
            "date": payment_date,
            "time": payment_time,
            "card": payment_card,
            "total_price": total_price,
            "items": items
        }
        return summary

    except Exception as e:
        # 예외 발생 시 에러 메시지 반환
        return {"알 수 없는 에러": str(e)}