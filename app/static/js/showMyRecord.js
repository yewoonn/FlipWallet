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
            if (data && data.categories && data.categories.length > 0) {
                const recordGrid = document.querySelector(".record-grid");
                recordGrid.innerHTML = ''; // 기존 기록 초기화

                // 각 카테고리별 기록을 카드 형태로 표시
                data.categories.forEach((category) => {
                    const categoryHTML = `
                        <div class="category-card">
                            <div class="card-header">
                                <span class="dot" style="background-color: ${category.color};"></span>
                                <span class="name">${category.category_name}</span>
                            </div>
                            <div class="card-body">
                                <p><strong>예산:</strong> ${category.budget}만원</p>
                                <p><strong>지출 금액:</strong> ${category.semi_expense}만원</p>
                                <p><strong>잔여 금액:</strong> ${category.semi_remaining}만원</p>
                                <p><strong>초과 금액:</strong> ${category.semi_over}만원</p>
                            </div>
                        </div>
                    `;
                    recordGrid.insertAdjacentHTML("beforeend", categoryHTML);
                });
            } else {
                console.error("기록이 없습니다.", data);
            }
        })
        .catch(error => {
            console.error("데이터 가져오기 오류:", error);
        });
});
