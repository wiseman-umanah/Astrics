$(document).ready(() => {
    const title = "Explore The Cosmos";
    const charArray = [...title];
    
    $('.bx-menu').on('click',
        function() {
            $('.nav-bar').toggle('slow');
            $('.bx-menu').toggle('slow');
            $('.bx-x').toggle('slow');
        }
    );
    $('.bx-x').on('click',
        function() {
            $('.nav-bar').toggle('slow');
            $('.bx-menu').toggle('slow');
            $('.bx-x').toggle('slow');
        }
    );
    let currentIndex = 0;

    function appendNextChar() {
        if (currentIndex < charArray.length) {
            $('.startup-title').append(charArray[currentIndex]);
            currentIndex++;
            setTimeout(appendNextChar, 100); // Adjust the interval (in milliseconds) as needed
        }
    }

    appendNextChar();
});
