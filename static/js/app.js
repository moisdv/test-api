const chatButton = document.querySelector('.chatbox__button');
const chatContent = document.querySelector('.chatbox__support');
const icons = {
    isClicked: '<img src="./static/icons/icon.png" width = "30px" height = "30px"/> ',
    isNotClicked: '<img src="./static/icons/icon.png" width = "30px" height = "30px"/>'
}
const chatbox = new InteractiveChatbox(chatButton, chatContent, icons);
chatbox.display();
chatbox.toggleIcon(false, chatButton);
