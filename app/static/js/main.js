document.addEventListener("DOMContentLoaded", () => {
    const writeExpenseButton = document.getElementById("write-expense-button");
    const viewExpenseButton = document.getElementById("view-expense-button");
    const setGoalButton = document.getElementById("set-goal-button");
    const viewGoalButton = document.getElementById("view-goal-button");
  
    writeExpenseButton.addEventListener("click", () => {
        window.location.href = "/writeExpense";
    });
  
    viewExpenseButton.addEventListener("click", () => {
      window.location.href = "/showMyRecord";
    });
  
    setGoalButton.addEventListener("click", () => {
      window.location.href = "/setSemiGoal";
    });
  
    viewGoalButton.addEventListener("click", () => {
      window.location.href = "/viewGoal";
    });
  });
  