import React, { useEffect, useState } from "react";
import Compose from "../Compose";
import Toolbar from "../Toolbar";
import Message from "../Message";
import moment from "moment";

import "./MessageList.css";

const MY_USER_ID = global.ValidatedUser;
let convoTitle = "Conversation with ...";
let SenderId = -1;
let ReceiverId = -1;

export default function MessageList(props) {
  let { sender, receiver } = props;

  const [messages, setMessages] = useState([]);
  useEffect(() => {
    if (receiver !== -1 && sender !== -1) {
      //TODO: get-user for each, extract names
      convoTitle = "Conversation with " + receiver;
      getMessages();
    }
  }, []);

  const getMessages = () => {
    var tempMessages = [
      {
        SenderId: 1,
        RecieverId: 2,
        Message: "message1",
        TimeStamp: "2019-10-24T20:23:50"
      },
      {
        SenderId: 2,
        RecieverId: 1,
        Message: "message2",
        TimeStamp: "2019-10-24T20:23:52"
      },

      {
        SenderId: 1,
        RecieverId: 2,
        Message: "message3",
        TimeStamp: "2019-10-24T21:23:54"
      },

      {
        SenderId: 2,
        RecieverId: 1,
        Message: "message4",
        TimeStamp: "2019-10-24T21:23:55"
      },

      {
        SenderId: 1,
        RecieverId: 2,
        Message: "message5",
        TimeStamp: "2019-10-24T21:23:57"
      },

      {
        SenderId: 2,
        RecieverId: 1,
        Message: "message6",
        TimeStamp: "2019-10-24T21:23:59"
      }
    ];

    setMessages([...messages, ...tempMessages]);
  };

  const renderMessages = () => {
    let i = 0;
    let messageCount = messages.length;
    let tempMessages = [];

    while (i < messageCount) {
      ReceiverId = messages[i].RecieverId;
      let previous = messages[i - 1];
      let current = messages[i];
      let next = messages[i + 1];
      let isMine = current.SenderId === MY_USER_ID;
      let currentMoment = moment(current.TimeStamp);
      let prevBySameAuthor = false;
      let nextBySameAuthor = false;
      let startsSequence = true;
      let endsSequence = true;
      let showTimestamp = true;

      if (previous) {
        let previousMoment = moment(previous.TimeStamp);
        let previousDuration = moment.duration(
          currentMoment.diff(previousMoment)
        );
        prevBySameAuthor = previous.SenderId === current.SenderId;

        if (prevBySameAuthor && previousDuration.as("hours") < 1) {
          startsSequence = false;
        }

        if (previousDuration.as("hours") < 1) {
          showTimestamp = false;
        }
      }

      if (next) {
        let nextMoment = moment(next.TimeStamp);
        let nextDuration = moment.duration(nextMoment.diff(currentMoment));
        nextBySameAuthor = next.SenderId === current.SenderId;

        if (nextBySameAuthor && nextDuration.as("hours") < 1) {
          endsSequence = false;
        }
      }

      tempMessages.push(
        <Message
          key={i}
          isMine={isMine}
          startsSequence={startsSequence}
          endsSequence={endsSequence}
          showTimestamp={showTimestamp}
          data={current}
        />
      );

      // Proceed to the next message.
      i += 1;
    }

    return tempMessages;
  };

  return (
    <div className="message-list">
      <Toolbar title={convoTitle} />

      <div className="message-list-container">{renderMessages()}</div>
      <Compose
        sender={SenderId}
        receiver={ReceiverId}
        validConvo={ReceiverId !== -1}
      />
    </div>
  );
}
