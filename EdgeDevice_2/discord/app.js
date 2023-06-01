import "dotenv/config";
import express from "express";
import { InteractionType, InteractionResponseType } from "discord-interactions";
import { VerifyDiscordRequest, getRandomEmoji } from "./utils.js";
import { connect } from "mqtt"; // import connect from mqtt
import { commands } from "./commands.js";

const app = express();

const PORT = process.env.PORT || 3000;

// Parse request body and verifies incoming requests using discord-interactions package
app.use(express.json({ verify: VerifyDiscordRequest(process.env.PUBLIC_KEY) }));

const client = connect("mqtt://test.mosquitto.org"); // create a client

/**
 * Interactions endpoint URL where Discord will send HTTP requests
 */
app.post("/interactions", async function (req, res) {
  // Interaction type and data
  const { type, data } = req.body;

  /**
   * Handle verification requests
   */
  if (type === InteractionType.PING) {
    return res.send({ type: InteractionResponseType.PONG });
  }

  /**
   * Handle slash command requests
   * See https://discord.com/developers/docs/interactions/application-commands#slash-commands
   */
  if (type === InteractionType.APPLICATION_COMMAND) {
    const { name } = data;

    // "test" command
    if (name === "test") {
      // Send a message into the channel where command was triggered from
      return res.send({
        type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        data: {
          // Fetches a random emoji to send from a helper function
          content: "hello world " + getRandomEmoji(),
        },
      });
    }

    // "command" command
    if (name === "command") {
      const command = req.body.data.options[0].value;
      const { topic, payload } = commands[command];
      client.publish(topic, String(payload));

      return res.send({
        type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        data: {
          content: `Command Received: ` + command,
        },
      });
    }
  }
});

app.listen(PORT, () => {
  console.log("Listening on port", PORT);
});
