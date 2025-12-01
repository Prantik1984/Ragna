(function () {
  "use strict";

  angular
    .module("ragApp", [])
    .controller("MainCtrl", ["$scope", "$timeout","$http", function ($scope, $timeout,$http) {
      var vm = this;

      vm.activePage = "home";
      vm.AppName = "Ragna";
      vm.selectedFile = null;
      vm.errorMessage=null;
      vm.isUploading=false;
      vm.chatdocument="";
      vm.chatResult="";
      vm.loadingMessage="";
      vm.uploadedFiles=[]
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
          console.log("Please select a file first.");
          return;
        }
        
        vm.isUploading=true;
        vm.loadingMessage="Uploading...";
        var formData = new FormData();
        formData.append("file", vm.selectedFile, vm.selectedFile.name);
        $http.post("http://127.0.0.1:9000/upload/pdfs", formData, {
    transformRequest: angular.identity,   
    headers: { "Content-Type": undefined } 
  })
  .then(function (response) {
    vm.isUploading=false;
    if(response.data.uploaded==true)
    {
      console.log("Uploadeddd");
      console.log("Upload success:", response.data);
      vm.setActive("chat");
      vm.chatdocument=response.data.id;
    }
    else
    {
      vm.errorMessage=response.data.error;
    }
    
  })
  .catch(function (error) {
    vm.isUploading=false;
    vm.errorMessage=error;
    console.log(error);
  });
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

      vm.selectQueryAbleFile=function(docName){
        
        for(const doc of vm.uploadedFiles)
        {
          doc.IsChecked=doc.Document==docName;
          
          
        }
        vm.selectedQueryFile = docName;
        // return false;
        // vm.selectedQueryFile = docName;
        // console.log(docName);
        // for(const doc of vm.uploadedFiles)
        // {
        //   doc.IsChecked=doc.Document==docName;
        //   return true;
          
        // }
        // return false;
      }

      vm.setActive = function (id) {
        vm.activePage = id;
        switch(vm.activePage)
        {
          case "chat":
            {
              vm.isUploading=true;
              vm.loadingMessage="Fetching documents...";

              $http.get("http://127.0.0.1:9000/listdocuments")
          .then(function (response) {
            vm.isUploading=false;
            if(response.data.Error)
            {
              vm.errorMessage=response.data.Error;
              return;
            }
            else
            {
              vm.uploadedFiles=[];
              var cnt=0;
              for(const doc of response.data.Sources)
              {
                vm.uploadedFiles.push({
                  "Document":doc,
                  "IsChecked":cnt==0
                });
                cnt++;
              }
             //vm.uploadedFiles=response.data.Sources;
             //console.log(vm.uploadedFiles);   
            }
          })
          .catch(function (error) {
            vm.isUploading=false;
      vm.errorMessage=error;
      console.error("Error:", error);        
          });
              break;
            }
        }
      };

      vm.exampleClick = function (q) {
        vm.currentQuestion = q;
      };

      vm.ask = function () {
        if (!vm.currentQuestion) {
          vm.errorMessage="Enter a question in the field";
          return;
        }
        
        var payload = {
    document: vm.chatdocument+".pdf",
    question: vm.currentQuestion
  };
  vm.isUploading=true;
  vm.loadingMessage="Fetching answer...";
  $http.post("http://127.0.0.1:9000/querydocument", payload)
    .then(function (response) {
      vm.isUploading=false;
      vm.chatResult=response.data;
    })
    .catch(function (error) {
      vm.isUploading=false;
      vm.errorMessage=error;
      console.error("Error:", error);
    });
      };

      
    }]);
})();
