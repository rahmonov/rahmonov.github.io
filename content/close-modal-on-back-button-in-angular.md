Title: Close modal on back button in AngularJS
Date: 2015-10-03 21:14
Modified: 2015-10-03 21:14
Category: programming
Tags: javascript, angularjs, modal
Slug: close-modal-on-back-button
Authors: Jahongir Rahmonov
Summary: How to close modal on back button in AngularJS without going back in browser history

We, developers, use modals all the time. I personally like to use [ngDialog](https://github.com/likeastore/ngDialog).

It is light, easy to use and highly customizable. [Bootstrap](https://angular-ui.github.io/bootstrap/#/modal) is also good but 
it is somewhat heavy.

Here is how modal is opened in ngDialog:

    :::javascript
    ngDialog.open({
        template: 'externalTemplate.html',
        controller: 'SomeController'
    });

It will open up a modal as expected but when you press the back button of the browser, what happens?
 
I would expect the modal to close and stay where I was before the modal. But what happens is that you go
back in browser history. Ouch! Especially on mobile, it is really not convenient to press the small 'x' button
of the modal. That's why, I would guess, user would press the back button to close the modal.

Here is how I solved the problem:

First, I created a service that deals with modals and it has a flag `modalIsShown` which will be used later:

    :::javascript
    myApp.service('ModalService', ['ngDialog', function (ngDialog) {
      var modalIsShown = false;

      var openModal = function (template, controller) {
        ngDialog.open({
          template: template,
          controller: controller,
          closeByDocument: false,
          closeByEscape: false,
          showClose: false
        });
      };

      var closeModal = function () {
        ngDialog.close();
      };

      return {
        openModal: openModal,
        closeModal: closeModal,
        modalIsShown: modalIsShown
      }
    }]);
    
Second, Here is how I open up a modal from my controller:

    :::javascript
    $scope.contactModal = function() {
      ModalService.modalIsShown = true;
      ModalService.openModal('contactModal.html', 'FooterController');
    };
    

Basically, the function sets the flag to true and opens the modal.

The most interestion part happens here:

    :::javascript
    myApp.run(['$rootScope', '$route', '$location', '$routeParams', 'ModalService',
      function($rootScope, $route, $location, $routeParams, ModalService) {

      $rootScope.$on('$routeChangeStart', function(evt, next, current) {
        if (ModalService.modalIsShown){
          ModalService.closeModal();
          ModalService.modalIsShown = false;
          evt.preventDefault();
        }
      });
    }]);
    
When a user presses a back button, when the url is about to change, angular calls this `$routeChangeStart`
observing function. And this function checks whether the flag `modalIsShown` is set to true. If so, it means
that a user is trying to close a modal by pressing the back button, thus it closes the modal, sets the flag
back to false and prevents the url change.

If anyone could suggest a better or cleaner way in comments, that would be awesome.

Hope it helps.

Fight on!



