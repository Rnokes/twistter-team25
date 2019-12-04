import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import Toolbar from "../Toolbar";
import axios from "axios";

import "./ConversationList.css";

export default function ConversationList() {
  const [conversations, setConversations] = useState([]);
  useEffect(() => {
    getConversations();
  }, []);

  const getConversations = () => {
    axios.get("https://randomuser.me/api/?results=20").then(response => {
      let newConversations = response.data.results.map(result => {
        return {
          name: `${result.name.first} ${result.name.last}`,
          text:
            "Hello world! This is a long message that needs to be truncated."
        };
      });
      setConversations([...conversations, ...newConversations]);
    });
  };

  return (
    <div className="conversation-list">
      <Toolbar title="MESSENGER" />
      {conversations.map(conversation => (
        //TODO: substitute conversation.name for new receiverId
        <Link
          to={{
            pathname: "/dm",
            state: { receiver: conversation.name }
          }}
        >
          <Button className="unstyled-button" variant="outline-dark">
            <h1 className="conversation-title">{conversation.name}</h1>
            <p className="conversation-snippet">{conversation.text}</p>
          </Button>
        </Link>
      ))}
    </div>
  );
}
