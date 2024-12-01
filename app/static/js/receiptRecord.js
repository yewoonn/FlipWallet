document.addEventListener("DOMContentLoaded", () => {
    const receiptInput = document.getElementById("receipt-input");
    const fileInfo = document.getElementById("file-info");
    const receiptImage = document.getElementById("receipt-image");
    const imagePreview = document.getElementById("image-preview");
    const submitButton = document.querySelector(".submit-button");

    let selectedFile = null; // 선택된 파일 저장

    // 파일 선택 시 처리
    receiptInput.addEventListener("change", () => {
        const file = receiptInput.files[0];
        selectedFile = file; // 선택된 파일 저장

        if (file) {
            fileInfo.textContent = `선택된 파일: ${file.name}`;

            // 이미지 미리보기
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
        formData.append("request_id", "12345"); // 선택적으로 추가
        formData.append("version", "V2"); // 선택적으로 추가

        try {
            const response = await fetch("/receipt", {
                method: "POST",
                body: formData,
            });
            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    alert("영수증 처리 성공!");
                    console.log("요약 데이터:", data.summary);
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
