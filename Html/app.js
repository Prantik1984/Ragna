(function () {
  "use strict";

  angular
    .module("ragApp", [])
    .controller("MainCtrl", function () {
      var vm = this;

      vm.activePage = "home";

      vm.navItems = [
        { id: "home", label: "Home", icon: "🏠" },
        { id: "upload", label: "Upload Document", icon: "📤" },
        { id: "chat", label: "Chat", icon: "💬" },
        { id: "settings", label: "Settings", icon: "⚙️" }
      ];

      vm.exampleQuestions = [
        "What is the project timeline?",
        "Who are the key stakeholders?",
        "Summarize the document"
      ];

      vm.recentDocuments = [
        { name: "Project_Plan.pdf", date: "Apr 10, 2024", citations: 8 },
        { name: "Financial_Report.pdf", date: "Mar 22, 2024", citations: 3 },
        { name: "Policy_Overview.txt", date: "Mar 5, 2024", citations: 3 }
      ];

      vm.setActive = function (id) {
        vm.activePage = id;
      };

      vm.exampleClick = function (q) {
        vm.currentQuestion = q;
      };

      vm.ask = function () {
        if (!vm.currentQuestion) {
          alert("Please type or choose a question first.");
          return;
        }
        alert("Question submitted: " + vm.currentQuestion);
      };
    });
})();
