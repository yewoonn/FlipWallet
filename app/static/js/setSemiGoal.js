const categories = [
        { id: 1, name: "자기계발", color: "#F25B5B" },
        { id: 2, name: "여가", color: "#F2815B" },
        { id: 3, name: "음식", color: "#F2DE5B" },
        { id: 4, name: "생활용품", color: "#B3F25B" },
        { id: 5, name: "교통", color: "#5BF2A4" },
        { id: 6, name: "쇼핑", color: "#5BEAF2" },
        { id: 7, name: "의료", color: "#5BB8F2" },
        { id: 8, name: "통신", color: "#8B5BF2" },
        { id: 9, name: "여행", color: "#F25BCC" },
        { id: 10, name: "이자", color: "#B3B3B3" },
        { id: 11, name: "구독 서비스", color: "#463E3E" }
    ];

document.addEventListener("DOMContentLoaded", () => {
    // 로그인 상태 확인
    const memberId = localStorage.getItem("member_id");
    const memberName = localStorage.getItem("member_name");

    // 사용자 정보 표시 영역
    const userInfoDisplay = document.getElementById("user-info");

    if (!memberId) {
        // 로그인되지 않은 상태면 로그인 페이지로 리다이렉트
        window.location.href = "/login";
    } else {
        // 로그인된 상태면 사용자 이름을 우측 상단에 표시
        if (userInfoDisplay) {
            userInfoDisplay.textContent = `안녕하세요, ${memberName}님!`;
        }
    }

    // 카테고리 관련 설정 및 나머지 로직
    const surplusInput = document.getElementById("surplus-input");
    const totalAmountDisplay = document.getElementById("total-amount");
    const submitButton = document.querySelector(".submit-button");
    const categoryList = document.querySelector(".category-list");

    // 카테고리 HTML 동적 생성
    categories.forEach((category) => {
      const categoryHTML = `
        <div class="category">
          <span class="dot" style="background-color: ${category.color};"></span>
          <span class="name">${category.name}</span>
          <div class="input-container">
            <input type="text" class="category-input" data-category-id="${category.id}" placeholder="카테고리 별 예산 입력">
            <p class="error-message" style="color: #E75C5C; font-size: 12px; display: none;">숫자만 입력 가능합니다</p>
          </div>
          <span>원</span>
        </div>
      `;
      categoryList.insertAdjacentHTML("beforeend", categoryHTML); // HTML 추가
    });

    const categoryInputs = document.querySelectorAll(".category-input");

    // 총 금액 계산 함수
    function calculateTotal() {
      let total = 0;

      // 카테고리 입력 값 합산
      categoryInputs.forEach((input) => {
        const value = parseFloat(input.value) || 0; // 값이 없으면 0으로 처리
        total += value;
      });

      // 비상금 입력 값 합산
      const surplusValue = parseFloat(surplusInput.value) || 0;
      total += surplusValue;

      // 총 금액 표시
      totalAmountDisplay.textContent = total.toLocaleString(); // 3자리 콤마 추가
    }

    // 입력값 확인 함수
    function validateInput(input) {
      const value = input.value;
      const errorMessage = input.parentNode.querySelector(".error-message");

      // 숫자가 아닌 문자가 포함되었는지 확인
      if (/[^0-9]/.test(value)) {
        input.classList.add("error"); // 에러 스타일 추가
        input.value = value.replace(/[^0-9]/g, ""); // 숫자 외의 값 제거
        if (errorMessage) {
          errorMessage.style.display = "block"; // 에러 메시지 표시
        }
      } else {
        input.classList.remove("error"); // 에러 스타일 제거
        if (errorMessage) {
          errorMessage.style.display = "none"; // 에러 메시지 숨김
        }
      }
    }

    // 입력 필드 값 변경 시 총 금액 재계산 및 유효성 검사
    categoryInputs.forEach((input) => {
      input.addEventListener("input", () => {
        validateInput(input);
        calculateTotal();
      });
    });

    surplusInput.addEventListener("input", () => {
      calculateTotal(); // 비상금 입력은 에러 검사가 필요 없음
    });

    // "기록 완료" 버튼 클릭 시 동작
    submitButton.addEventListener("click", () => {
      const categoryData = Array.from(categoryInputs).map((input) => ({
        category_id: parseInt(input.getAttribute("data-category-id")), // category_id 사용
        budget: parseFloat(input.value) || 0 // float 형식으로 변환
      }));
      const surplusBudget = parseFloat(surplusInput.value) || 0.0;

      const data = {
        member_id: memberId,  // member_id를 포함해 전송
        categories: categoryData,
        surplus_budget: surplusBudget
      };

      console.log("전송할 데이터:", data); // 전송할 데이터를 로그로 출력

      // 서버로 데이터 전송 (POST 요청)
      fetch("/setSemiGoal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      })
      .then(response => {
        console.log("서버 응답 상태 코드:", response.status); // 서버 응답 코드 로그 출력
        return response.json().then(data => {
          if (response.ok) {
            window.location.href = "/showMyRecord"; // 데이터가 성공적으로 저장되면 다음 페이지로 이동
          } else {
            console.error("응답 오류 데이터:", data); // 오류 데이터 로그 출력
            alert(data.detail || "목표 설정에 실패했습니다.");
          }
        });
      })
      .catch(error => {
        console.error("통신 오류:", error); // 통신 오류 로그 출력
        alert("서버와 통신 중 오류가 발생했습니다.");
      });
    });
});
