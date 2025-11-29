const sceneElement = document.getElementById("scene");
const speakerElement = document.getElementById("speaker");
const dialogueElement = document.getElementById("dialogue");
const promptElement = document.getElementById("prompt");
const choicesContainer = document.getElementById("choices");
const historyList = document.getElementById("history");
const backgroundLayer = document.getElementById("background");

let storyData = null;
let currentSceneId = null;
const historyItems = [];

function setScene(sceneId) {
  currentSceneId = sceneId;
  const scene = storyData.scenes[sceneId];

  speakerElement.textContent = scene.speaker;
  dialogueElement.textContent = scene.dialogue;
  promptElement.textContent = scene.prompt ?? "배경 프롬프트가 준비 중이에요.";
  backgroundLayer.style.background = scene.background;

  const historyEntry = document.createElement("li");
  historyEntry.textContent = `${scene.speaker}: ${scene.dialogue}`;
  historyItems.push(historyEntry);
  historyList.replaceChildren(...historyItems.slice(-8));

  renderChoices(scene.choices);
}

function renderChoices(choices) {
  choicesContainer.innerHTML = "";

  if (!choices.length) {
    const endMessage = document.createElement("p");
    endMessage.className = "end-text";
    endMessage.textContent = "이야기가 끝났어요. 새로고침으로 다시 시작!";
    choicesContainer.appendChild(endMessage);
    return;
  }

  choices.forEach((choice) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = choice.text;
    button.addEventListener("click", () => setScene(choice.next));
    choicesContainer.appendChild(button);
  });
}

async function loadStory() {
  const response = await fetch("/api/story");
  storyData = await response.json();
  setScene(storyData.start);
}

loadStory();
