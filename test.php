<html>
    <head>
        <title>CGI Binary Demo</title>
    </head>
    <body>
        <h1>Welcome To Group 16</h1>
        <p>This demo is to demonstrate how the game client will communicate to the python scripts</p>
        <p>This file represents the game engine client</p>
        <p>This file will send the message typed below as a http get parameter with the name "message" to https://fathomless.io/cgi-bin/test.cgi</p>

        <input oninput = "testCommunication(this.value)" placeholder = "Type a message">
        
        <p>https://fathomless.io/cgi-bin/test.cgi will then recive the message and perform the test opperation upon the message</p>
        <p>The python script will respond back with the length of the message string as shown below</p>
        <p>The server response is: <span id = "response"></span></p>

        <script>
            function testCommunication(message) {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById('response').innerHTML = this.responseText;
                    }
                  }
                  xmlhttp.open("GET", "https://fathomless.io/cgi-bin/test.cgi?message="+encodeURIComponent(message), true);
                  xmlhttp.send();
            }
        </script>
    </body>
</html>
