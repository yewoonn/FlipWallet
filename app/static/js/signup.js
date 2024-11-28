document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm-password");
    const errorMessage = document.getElementById("errorMessage");

    // 비밀번호 확인 입력 시 실시간 검사
    confirmPasswordInput.addEventListener("input", () => {
        if (passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.classList.add("error");
            errorMessage.style.display = "block";
        } else {
            confirmPasswordInput.classList.remove("error");
            errorMessage.style.display = "none";
        }
    });

    // 폼 제출 시 JSON으로 회원가입 처리
    form.addEventListener("submit", (event) => {
        event.preventDefault(); // 폼의 기본 동작 막기

        // JSON 데이터 객체 생성
        const formData = new FormData(form);
        const data = {
            name: formData.get("name"),
            email: formData.get("email"),
            login_id: formData.get("id"),
            password: formData.get("password"),
            confirm_password: formData.get("confirm-password")
        };

        // 비밀번호 일치 여부 확인
        if (data.password !== data.confirm_password) {
            confirmPasswordInput.classList.add("error");
            errorMessage.textContent = "Passwords do not match.";
            errorMessage.style.display = "block";
            return;
        }

        // AJAX 요청을 통해 회원가입 처리 (JSON으로 보내기)
        fetch("/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data) // JSON 문자열로 변환하여 서버에 전송
        })
        .then(response => {
            if (response.redirected) {
                // 리다이렉트가 발생한 경우 리다이렉션 URL로 이동
                window.location.href = response.url;
            } else if (!response.ok) {
                // 실패 시 에러 메시지를 보여줌
                response.json().then(data => {
                    errorMessage.textContent = data.detail || "회원가입에 실패했습니다.";
                    errorMessage.style.display = "block";
                });
            }
        })
        .catch(error => {
            errorMessage.textContent = "서버와 통신 중 오류가 발생했습니다.";
            errorMessage.style.display = "block";
        });
    });
});