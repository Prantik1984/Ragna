(function () {
  "use strict";

  angular
    .module("ragApp", [])
    .controller("MainCtrl", ["$scope", "$timeout", function ($scope, $timeout) {
      var vm = this;

      vm.activePage = "home";
      vm.AppName = "Ragna";
      vm.selectedFile = null;

      vm.navItems = [
        { id: "home", label: "Home", icon: "🏠" },
        { id: "upload", label: "Upload Document", icon: "📤" },
        { id: "chat", label: "Chat", icon: "💬" },
        { id: "settings", label: "Settings", icon: "⚙️" }
      ];

      // Open file picker
      vm.selectFile = function () {
        var input = document.getElementById("fileInput");
        if (input) {
          input.click();
        }
      };

      // Called when user clicks Upload
      vm.uploadFile = function () {
        if (!vm.selectedFile) {
          alert("Please select a file first.");
          return;
        }
        console.log("Uploading:", vm.selectedFile.name);
        // TODO: your actual upload logic here
      };

      // Attach change handler AFTER DOM is ready
      $timeout(function () {
        var input = document.getElementById("fileInput");
        if (!input) return;

        input.addEventListener("change", function (event) {
          var file = event.target.files[0];
          if (file) {
            // Use $scope.$apply so Angular updates bindings
            $scope.$apply(function () {
              vm.selectedFile = file;
              console.log("Selected file:", file.name);
            });
          }
        });
      });

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
    }]);
})();
