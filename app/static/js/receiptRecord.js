document.addEventListener("DOMContentLoaded", () => {
    const receiptInput = document.getElementById("receipt-input");
    const fileInfo = document.getElementById("file-info");
    const receiptImage = document.getElementById("receipt-image");
    const imagePreview = document.getElementById("image-preview");
  
    // 파일 선택 시 처리
    receiptInput.addEventListener("change", () => {
      const file = receiptInput.files[0];
  
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
  });
  