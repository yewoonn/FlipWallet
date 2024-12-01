document.addEventListener("DOMContentLoaded", () => {
    const writeExpenseButton = document.getElementById("write-expense-button");
    const viewExpenseButton = document.getElementById("view-expense-button");
    const setGoalButton = document.getElementById("set-goal-button");
    // const viewGoalButton = document.getElementById("view-goal-button");


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

    // 목표 정하기
    setGoalButton.addEventListener("click", () => {
      window.location.href = "/setSemiGoal";
    });

    // 지출 작성하기
    writeExpenseButton.addEventListener("click", () => {
        window.location.href = "/writeExpense";
    });


    // 나의 지출 기록 조회
    viewExpenseButton.addEventListener("click", () => {
      window.location.href = "/showMyRecord";
    });


  });
  