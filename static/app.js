const sceneElement = document.getElementById("scene");
const speakerElement = document.getElementById("speaker");
const dialogueElement = document.getElementById("dialogue");
const promptElement = document.getElementById("prompt");
const choicesContainer = document.getElementById("choices");
const historyList = document.getElementById("history");
const backgroundLayer = document.getElementById("background");
const llmForm = document.getElementById("llmForm");
const llmPromptInput = document.getElementById("llmPrompt");
const llmThinkingInput = document.getElementById("llmThinking");
const llmEffortSelect = document.getElementById("llmEffort");
const llmStatus = document.getElementById("llmStatus");
const llmResult = document.getElementById("llmResult");

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

async function requestLLM(payload) {
  const response = await fetch("/api/llm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return response.json().then((data) => ({ ok: response.ok, data }));
}

if (llmForm) {
  llmForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const prompt = llmPromptInput.value.trim();
    if (!prompt) {
      llmStatus.textContent = "프롬프트를 입력해 주세요.";
      return;
    }

    const useThinking = llmThinkingInput?.checked;
    const reasoningEffort = llmEffortSelect?.value || "medium";

    const payload = {
      prompt,
      use_thinking: useThinking,
      reasoning_effort: reasoningEffort,
    };

    llmStatus.textContent = "LM Studio에 요청 중...";
    llmResult.textContent = "";
    llmForm.querySelector("button").disabled = true;

    try {
      const { ok, data } = await requestLLM(payload);
      if (ok && data.response) {
        llmStatus.textContent = "완료!";
        llmResult.textContent = data.response;
      } else {
        llmStatus.textContent = data.error || "문장을 불러오지 못했어요.";
        llmResult.textContent = data.detail || "";
      }
    } catch (error) {
      console.error(error);
      llmStatus.textContent = "요청 중 문제가 발생했어요.";
    } finally {
      llmForm.querySelector("button").disabled = false;
    }
  });
}
