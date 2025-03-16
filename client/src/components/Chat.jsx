import { useLocation } from "react-router";
import { useState } from "react";
export default function Chat() {
  const location = useLocation();
  const responseData = location.state?.responseData;
  const initialMessages = [
    {
      "role": "assistant",
      "message": responseData.message,
    },
  ];
  console.log("Chat rerendered with", responseData);
  const [chatMessages, setChatMessages] = useState(initialMessages);
  const [newMessage, setNewMessage] = useState("");

  const handleInput = (e) => {
    setNewMessage(e.target.value);
  };

  const handleSend = () => {
    if (newMessage.trim()) {
      setChatMessages([...chatMessages, { role: "user", message: newMessage }]);
      setNewMessage("");
    }
  };

  return (
    <div>
      <h1>Chat</h1>
      <div>
        {chatMessages.map((message, index) => (
          <div key={index}>
            <p>{message.role}</p>
            <p>{message.message}</p>
          </div>
        ))}
      </div>
      <input type="text" onChange={handleInput} value={newMessage} />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
