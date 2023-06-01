import "dotenv/config";
import { InstallGlobalCommands } from "./utils.js";

export const commands = {
  "Buzzer ON": {
    payload: 3,
    topic: "SmokeBuzzer",
  },
  "Buzzer OFF": {
    payload: 4,
    topic: "SmokeBuzzer",
  },
  "Fan ON": {
    payload: 3,
    topic: "ThermoFan",
  },
  "Fan OFF": {
    payload: 4,
    topic: "ThermoFan",
  },
  "Temperature LED ON": {
    payload: 1,
    topic: "ThermoLed",
  },
  "Temperature LED OFF": {
    payload: 2,
    topic: "ThermoLed",
  },
  "Smoke LED ON": {
    payload: 1,
    topic: "SmokeLed",
  },
  "Smoke LED OFF": {
    payload: 2,
    topic: "SmokeLed",
  },
  "Motion LED ON": {
    payload: 1,
    topic: "MotionLed",
  },
  "Motion LED OFF": {
    payload: 2,
    topic: "MotionLed",
  },
};

// Get the game choices from game.js
function createCommandChoices() {
  const commandChoices = [];

  for (let choice of Object.keys(commands)) {
    commandChoices.push({
      name: choice,
      value: choice,
    });
  }
  return commandChoices;
}

// Simple test command
const TEST_COMMAND = {
  name: "test",
  description: "Basic command",
  type: 1,
};

// Command containing options
const COMMAND_COMMAND = {
  name: "command",
  description: "Send a command to an actuator",
  options: [
    {
      type: 3,
      name: "command",
      description: "Pick your command",
      required: true,
      choices: createCommandChoices(),
    },
  ],
  type: 1,
};

const ALL_COMMANDS = [TEST_COMMAND, COMMAND_COMMAND];

InstallGlobalCommands(process.env.APP_ID, ALL_COMMANDS);
