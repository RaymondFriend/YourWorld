var topic = ""

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

    // Request assistant's response
    const assistantResponse = assistant_respond(userInput)
    assistant_respond(userInput)
    .then(output => {
        console.log("Received output:", output);
        addMessageToChat(output, 'assistant');
    })
    .catch(error => {
        console.error("Error:", error);
        addMessageToChat("HTML error: " + error, 'assistant');
    });
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

// converts the formatted string default from newsapi to more readable
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
    topic = searchQuery // this updates a global variable so that the AI might also have access to the current topic

    /* Now we may process the searchQuery
        I'm thinking of having an AI basically fix any typos by asking it nicely.

        Here are the only restrictions on the query (q) when we do an everything search:
            Surround phrases with quotes (") for exact match.
            Prepend words or phrases that must appear with a + symbol. Eg: +bitcoin
            Prepend words that must not appear with a - symbol. Eg: -bitcoin
            Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis. Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.
            The complete value for q must be URL-encoded. Max length: 500 chars.
    */

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

// Function to perform the search and fetch articles
function assistant_respond(input) {

    /* Now we may process the input
        1. Process the input so it's grammatically correct (that'll be a specially trained AI)
        2. Run classification to understand what kind of request this is between ['conversational task', 'summarization task', 'translation task', 'analyzing sentiment task]
        3. Map those options to ['conversational', 'summarization', 'translation', 'sentiment-analysis'], for which we have a model already instantiated
        4. Depending on the task, the inputs will be processed slightly differently. But for now no worries.
        5. Output the corresponding response as the assistant's response to be displayed up the chain.
    */

    return new Promise((resolve, reject) => {
        fetch('http://127.0.0.1:5000/AI_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: input }),
        })
        .then(response => response.json()) 
        .then(data => {
            console.log("the output received from JSON is: " + data.output); 
            resolve(data.output);
        })
        .catch(error => {
            console.error('Error:', error);
            reject(error);
        });
    })
}
