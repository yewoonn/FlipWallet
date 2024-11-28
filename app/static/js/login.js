document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".login-form");
    const errorMessage = document.getElementById("errorMessage");

    if (form) {
        form.addEventListener("submit", (event) => {
            event.preventDefault();  // 기본 폼 제출 방지

            const formData = new FormData(form);
            const data = {
                login_id: formData.get("login_id"),
                password: formData.get("password")
            };

            fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (response.ok) {
                    response.json().then(data => {
                        // 로그인 성공 시 사용자 정보 LocalStorage에 저장
                        localStorage.setItem("member_id", data.member_id);
                        localStorage.setItem("member_name", data.name);
                        window.location.href = data.redirect_url;  // 리다이렉트 URL로 이동
                    });
                } else {
                    response.json().then(data => {
                        if (errorMessage) {
                            errorMessage.textContent = data.detail || "로그인에 실패했습니다.";
                            errorMessage.style.display = "block";
                        }
                    });
                }
            })
            .catch(error => {
                if (errorMessage) {
                    errorMessage.textContent = "서버와 통신 중 오류가 발생했습니다.";
                    errorMessage.style.display = "block";
                }
            });
        });
    }
});
