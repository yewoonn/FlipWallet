document.addEventListener("DOMContentLoaded", () => {
    const writeExpenseButton = document.getElementById("write-expense-button");
    const viewExpenseButton = document.getElementById("view-expense-button");
    const setGoalButton = document.getElementById("set-goal-button");
    const viewGoalButton = document.getElementById("view-goal-button");
  
    writeExpenseButton.addEventListener("click", () => {
      window.location.href = "writeExpense.html"; 
    });
  
    viewExpenseButton.addEventListener("click", () => {
      window.location.href = "showMyRecord.html"; 
    });
  
    setGoalButton.addEventListener("click", () => {
      window.location.href = "setSemiGoal.html"; 
    });
  
    viewGoalButton.addEventListener("click", () => {
      window.location.href = "viewGoal.html"; 
    });
  });
  