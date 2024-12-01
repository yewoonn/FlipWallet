document.addEventListener("DOMContentLoaded", () => {
    const categories = [
        { id: 1, name: "자기계발" },
        { id: 2, name: "여가" },
        { id: 3, name: "음식" },
        { id: 4, name: "생활용품" },
        { id: 5, name: "교통" },
        { id: 6, name: "쇼핑" },
        { id: 7, name: "의료" },
        { id: 8, name: "통신" },
        { id: 9, name: "여행" },
        { id: 10, name: "이자" },
        { id: 11, name: "구독 서비스" },
    ];

    // 요소 선택
    const receiptInput = document.getElementById("receipt-input");
    const fileInfo = document.getElementById("file-info");
    const receiptImage = document.getElementById("receipt-image");
    const submitButton = document.querySelector(".submit-button");
    const categorySelect = document.getElementById("category-select");

    let selectedFile = null; // 선택된 파일 저장
    let recognizedItem = ""; // OCR로 인식된 지출 항목
    let recognizedPrice = 0; // OCR로 인식된 금액

    // 카테고리 옵션 추가
    categories.forEach((category) => {
        const option = document.createElement("option");
        option.value = category.id;
        option.textContent = category.name;
        categorySelect.appendChild(option);
    });

    // 파일 선택 시 이미지 미리보기 처리
    receiptInput.addEventListener("change", () => {
        const file = receiptInput.files[0];
        selectedFile = file;

        if (file) {
            fileInfo.textContent = `선택된 파일: ${file.name}`;
            const reader = new FileReader();
            reader.onload = function (e) {
                receiptImage.src = e.target.result;
                receiptImage.style.display = "block";
            };
            reader.readAsDataURL(file);
        } else {
            fileInfo.textContent = "선택된 파일 없음";
            receiptImage.style.display = "none";
        }
    });

    // 기록 완료 버튼 클릭 시 처리
    submitButton.addEventListener("click", async () => {
        if (!selectedFile) {
            alert("파일을 선택하세요.");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("request_id", "12345");
        formData.append("version", "V2");

        try {
            // Step 1: 영수증 OCR 요청
            const response = await fetch("/receipt", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();

                if (data.status === "success") {
                    const summary = data.summary;

                        // summary.items와 summary.total_price에서 데이터 가져오기
                        if (summary.items && summary.items.length > 0) {
                            recognizedItem = summary.items[0].name || "알 수 없는 항목"; // 첫 번째 아이템의 이름 사용
                            recognizedPrice = summary.total_price || 0; // 총 금액 사용
                        } else {
                            alert("영수증에서 항목을 인식하지 못했습니다. 직접 입력하거나 다시 시도해 주세요.");
                            return;
                        }

                        // 유효성 체크 후 사용자에게 보여줌
                        if (recognizedPrice > 0) {
                            alert(`인식된 항목: ${recognizedItem}\n인식된 금액: ${recognizedPrice.toLocaleString()}원`);
                        } else {
                            alert("영수증에서 금액을 인식하지 못했습니다. 직접 입력하거나 다시 시도해 주세요.");
                            return;
                        }

                        // 사용자가 카테고리를 선택하고 최종 기록을 완료
                        const categoryId = parseInt(categorySelect.value, 10);
                        const memberId = localStorage.getItem("member_id");

                        if (isNaN(categoryId)) {
                            alert("카테고리를 선택하세요.");
                            return;
                        }

                        // 최종 지출 내역 기록
                        const expenseData = {
                            member_id: memberId,
                            category_id: categoryId,
                            item: recognizedItem,
                            price: recognizedPrice,
                        };

                    const expenseResponse = await fetch("/writeExpense", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(expenseData),
                    });

                    if (expenseResponse.ok) {
                        alert("지출 기록이 성공적으로 저장되었습니다.");
                        window.location.href = "/showMyRecord";
                    } else {
                        const errorData = await expenseResponse.json();
                        throw new Error(errorData.detail || "지출 기록에 실패했습니다.");
                    }
                } else {
                    alert(`영수증 처리 실패: ${data.message}`);
                }
            } else {
                alert(`서버 오류 발생: ${response.status}`);
            }
        } catch (error) {
            console.error("요청 오류:", error);
            alert("요청 중 오류가 발생했습니다.");
        }
    });
});
