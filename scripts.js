// Checking the server is handling OPTIONS requests
fetch('http://127.0.0.1:5000/', {
    method: 'OPTIONS',
})
.then(response => {
    if (response.status === 200) {
        console.log('OPTIONS request successful. CORS preflight check passed!');
    } else {
        console.error('OPTIONS request failed:', response.status);
    }
})
.catch(error => {
    console.error('Error during OPTIONS request:', error);
});


// Array to store chat messages
let chatMessages = [];

// Function to handle sending messages
function sendMessage() {
    const userInput = document.getElementById('userInput').value;

    if (userInput.trim() !== '') {
        addMessageToChat(userInput, 'user');
        document.getElementById('userInput').value = ''; // Clear the input field after sending the message
    }

    // Simulate assistant's response (replace with actual assistant logic)
    const assistantResponse = 'This is an assistant response.';
    addMessageToChat(assistantResponse, 'assistant');
    
}

// Function to add messages to the chat log
function addMessageToChat(message, senderType) {
    // Create a message object with text and senderType
    const newMessage = {
        text: message,
        sender: senderType,
    };

    // Add the message to the chat log
    chatMessages.push(newMessage);

    // Update the display
    displayChatMessages();
}

// Function to display chat messages in the chat display area
function displayChatMessages() {
    const chatDisplay = document.getElementById('chatDisplay');
    chatDisplay.innerHTML = ''; // Clear previous messages

    // Loop through the chatMessages array and display messages
    chatMessages.forEach((message) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add(message.sender === 'user' ? 'user-message' : 'assistant-message');
        messageElement.textContent = message.text;

        chatDisplay.appendChild(messageElement);
    });
}

// Function to handle "Return" key press in the text area
document.getElementById('userInput').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default behavior of Enter key (like adding a newline)
        sendMessage(); // Trigger sendMessage function when Enter is pressed
    }
});

function formatDateString(dateString) {
    try {
        const date = new Date(dateString);
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', timeZoneName: 'short' };
        return date.toLocaleDateString('en-US', options);
    } catch (error) {
        console.error('Error formatting date:', error);
        return dateString; // Return original date string if an error occurs
    }
}

// Function to perform the search and fetch articles
function searchArticles() {
    const searchQuery = document.getElementById('searchInput').value; // Get the search query from an input field

    // Make a POST request to your Flask API endpoint
    fetch('http://127.0.0.1:5000/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchQuery: searchQuery }), // Send the search query as JSON
    })
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
        // Handle the fetched articles (data.articles) returned from the Flask API
        // Display or process the articles as needed in your frontend
        console.log(data.articles); // For example, log the articles to the console
        
        // Display the first found article content in the article pane
        const articleContent = document.getElementById('articleContent');
        const articleTitle = document.getElementById('articleTitle');
        const articleDate = document.getElementById('articleDate');
        const articleURL = document.getElementById('articleURL');
        const articleImage = document.getElementById('articleImage');

        if (data.articles) {
            var i = 0;
            articleContent.textContent = data.articles[i]['content'];
            articleTitle.textContent = data.articles[i]['title'];
            articleDate.textContent = formatDateString(data.articles[i]['publishedAt']);
            articleURL.textContent = data.articles[i]['url'];
            const newImageURL = data.articles[i]['urlToImage'];
            articleImage.src = newImageURL;
        } else {
            articleContent.textContent = "No relevant article found.";
            articleTitle.textContent = "";
            articleDate.textContent = "";
            articleURL.textContent = "";
            articleImage.src = "";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
