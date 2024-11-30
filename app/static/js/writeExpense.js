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
    const categorySelect = document.getElementById("category-select");
    const submitButton = document.querySelector(".submit-button");
    const amountInput = document.getElementById("amount-input");
    const directInputButton = document.querySelector(".direct-input-button");
    const amountButtons = document.querySelectorAll(".amount-button");

    // 로그인된 사용자 정보
    const memberId = localStorage.getItem("member_id");
    const memberName = localStorage.getItem("member_name");

    // 사용자 이름 표시
    const userInfoDisplay = document.getElementById("user-info");
    if (userInfoDisplay && memberName) {
        userInfoDisplay.textContent = `안녕하세요, ${memberName}님!`;
    }

    // 카테고리 옵션 추가
    categories.forEach((category) => {
        const option = document.createElement("option");
        option.value = category.id; // id를 사용하여 서버로 전달
        option.textContent = category.name;
        categorySelect.appendChild(option);
    });

    // 금액 업데이트 함수
    function updateAmount(amount) {
        const currentAmount = parseInt(amountInput.value.replace(/,/g, ""), 10) || 0;
        const newAmount = currentAmount + amount;
        amountInput.value = newAmount.toLocaleString();
    }

    // 금액 버튼 클릭 이벤트
    amountButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const amount = parseInt(button.dataset.amount, 10);
            updateAmount(amount);
        });
    });

    // 직접 입력 버튼 클릭 이벤트
    directInputButton.addEventListener("click", () => {
        const manualAmount = prompt("금액을 입력하세요:");
        if (manualAmount !== null && !isNaN(manualAmount) && manualAmount >= 0) {
            amountInput.value = parseInt(manualAmount, 10).toLocaleString();
        } else {
            alert("올바른 금액을 입력하세요.");
        }
    });
    // 제출 버튼 클릭 이벤트
    submitButton.addEventListener("click", () => {
        // 사용자 입력 값 가져오기
        const item = document.getElementById("expense-item").value.trim();
        const categoryId = parseInt(categorySelect.value, 10);
        const price = parseFloat(amountInput.value.replace(/,/g, ""));

        // 입력 값 유효성 검사
        if (!item || isNaN(categoryId) || isNaN(price) || price <= 0) {
            alert("모든 항목을 올바르게 입력해주세요.");
            return;
        }

        // 서버로 전송할 데이터 구성
        const data = {
            member_id: memberId,
            category_id: categoryId,
            item: item,
            price: price
        };

        console.log("전송할 데이터:", JSON.stringify(data, null, 2)); // 데이터 확인 로그

        // 서버로 데이터 전송 (POST 요청)
        fetch("/writeExpense", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data) // JSON 형식으로 데이터를 보냅니다.
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(data => {
                    throw new Error(data.detail || "지출 기록에 실패했습니다.");
                });
            }
        })
        .then(data => {
            alert("지출 기록이 성공적으로 저장되었습니다.");
            window.location.href = "/showMyRecord"; // 성공적으로 저장된 후 페이지 이동
        })
        .catch(error => {
            console.error("통신 오류:", error); // 통신 오류 확인
            alert("서버와의 통신 중 오류가 발생했습니다.");
        });
    });
});
