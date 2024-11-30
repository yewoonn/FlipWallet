document.addEventListener("DOMContentLoaded", () => {
    const memberId = localStorage.getItem("member_id");
    const memberName = localStorage.getItem("member_name");

    // 로그인되지 않은 경우 로그인 페이지로 리다이렉트
    if (!memberId) {
        window.location.href = "/login";
    }

    // 사용자 이름을 우측 상단에 표시
    const userInfoDisplay = document.getElementById("user-info");
    if (userInfoDisplay && memberName) {
        userInfoDisplay.textContent = `안녕하세요, ${memberName}님!`;
    }

    // 나의 지출 기록을 가져와서 화면에 표시
    fetch(`/getMyRecord?member_id=${memberId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Received data: ", data); // 데이터 로깅
            const recordGrid = document.querySelector(".record-grid");

            if (data && data.categories && data.categories.length > 0) {
                recordGrid.innerHTML = ''; // 기존 기록 초기화

                data.categories.forEach((category) => {
                    const budget = category.budget !== undefined ? parseFloat(category.budget).toFixed(2) : "0.00";
                    const semiExpense = category.semi_expense !== undefined ? parseFloat(category.semi_expense).toFixed(2) : "0.00";
                    const semiRemaining = category.semi_remaining !== undefined ? parseFloat(category.semi_remaining).toFixed(2) : "0.00";
                    const semiOver = category.semi_over !== undefined ? parseFloat(category.semi_over).toFixed(2) : "0.00";

                    const categoryHTML = `
                        <div class="category-card">
                            <div class="card-header">
                                <span class="dot" style="background-color: ${category.color};"></span>
                                <span class="name">${category.category_name}</span>
                            </div>
                            <div class="card-body">
                                <p><strong>예산:</strong> ${budget} 만원</p>
                                <p><strong>지출 금액:</strong> ${semiExpense} 만원</p>
                                <p><strong>잔여 금액:</strong> ${semiRemaining} 만원</p>
                                <p><strong>초과 금액:</strong> ${semiOver} 만원</p>
                            </div>
                        </div>
                    `;
                    recordGrid.insertAdjacentHTML("beforeend", categoryHTML);
                });
            } else {
                console.error("기록이 없습니다.", data);
                recordGrid.innerHTML = '<p>기록이 없습니다. 세부 목표를 설정해 주세요.</p>';
            }
        })
        .catch(error => {
            console.error("데이터 가져오기 오류:", error);
            const recordGrid = document.querySelector(".record-grid");
            recordGrid.innerHTML = `<p>데이터를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.</p>`;
        });
});
