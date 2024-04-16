<script>
  import { afterUpdate, onMount } from "svelte";
  import { fade } from "svelte/transition";
  import { BACKEND_URL, QUIZ_PROMPT, BLOCK_FADE_IN_DELAY, BLOCK_FADE_IN_DURATION, BLOCK_FADE_OUT_DURATION } from "../constants";
  import LatexInterpreter from "./LatexInterpreter.svelte";

  export let username;
  export let topic;
  export let curriculum;
  export let curriculumHist;
  export let theme;
  export let block;
  export let finalTexts;
  export let displayTexts;
  export let changeFunFact;
  
  let writer;
  let doneWriting = true;
  let topicBlock;
  let userQueryInput;

  async function sendQuery(query) {
    finalTexts = [...finalTexts, query];
    displayTexts = [...displayTexts, query];

    let sendGptMsgResponse = await fetch(BACKEND_URL + "/sendGptMsg", {
      method: "POST",
      body: JSON.stringify({
        "topicId":  topic.topicId,
        "courseNumber": curriculum.curriculumId,
        "newMsg": query,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let sendGptMsgData = await sendGptMsgResponse.json();

    if (sendGptMsgData == "Processing") {
      let latestMsg = await recursiveGetLatestMsg(curriculum.curriculumId);
      latestMsg = latestMsg.chatHistory[latestMsg.chatHistory.length - 1][1];
      finalTexts = [...finalTexts, latestMsg];
      displayTexts = [...displayTexts, ""];
    }
  }

  async function getChatHistory(curriculumId) {
    let getChatHistoryResponse = await fetch(BACKEND_URL + "/getChatHistory", {
      method: "POST",
      body: JSON.stringify({
        "topicId":  topic.topicId,
        "courseNumber": curriculumId,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let getChatHistoryData = await getChatHistoryResponse.json();
    return getChatHistoryData;
  }

  async function delay(time) {
    return new Promise(res => {
      setTimeout(res,time)
    })
  }

  async function recursiveGetLatestMsg(curriculumId) {
    console.log("recursively getting latest msg")
    let chatHistory = await getChatHistory(curriculumId);
    
    if (chatHistory.chatHistory.length == finalTexts.length - 1) {
      await delay(4000);
      chatHistory = await recursiveGetLatestMsg(curriculumId);
    }
    return chatHistory;
  }

  async function recursiveGetChatHistory(curriculumId) {
    console.log("recursively getting ChatHistory")
    let chatHistory = await getChatHistory(curriculumId);
    
    if (chatHistory == "NoHistory") {
      await delay(4000);
      chatHistory = await recursiveGetChatHistory(curriculumId);
    }
    return chatHistory;
  }

  async function getOrGenerateCurriculum(curriculumId, curriculumName) {
    let chatHistory = await getChatHistory(curriculumId);
    
    if (chatHistory.chatHistory != null) {
      return {
        curriculumId: curriculumId,
        curriculumName: curriculumName,
        chatHistory: chatHistory.chatHistory,
      }
    } else if (chatHistory == "NoHistory") {
      let generateCourseResponse = await fetch(BACKEND_URL + "/generateCourse", {
        method: "POST",
        body: JSON.stringify({
          "topicId":  topic.topicId,
          "courseNumber": curriculumId,
        }),
        headers: {
          "authorizationUserLoginToken": "qwertyuiop:" + username,
        }
      });

      let generateCourseData = await generateCourseResponse.json();
      if (generateCourseData == "Generating Course") {
        let chatHistory = await recursiveGetChatHistory(curriculumId);
        
        return {
          curriculumId: curriculumId,
          curriculumName: curriculumName,
          chatHistory: chatHistory.chatHistory,
        }
      }
    }
  }
    
  async function changeTopic(curriculumId, curriculumName) {
    block = "loading";
    changeFunFact(curriculumName)
    curriculumHist = null;

    curriculum = await getOrGenerateCurriculum(curriculumId, curriculumName);

    block = "topic-block";
    finalTexts = [];
    curriculum.chatHistory.forEach((msg) => {
      finalTexts = [...finalTexts, msg[1]];
    })

    if (finalTexts.length == 1) { // new chat show typewriter
      displayTexts = [""];
    } else {
      displayTexts = [...finalTexts];
    }
  }

  function showText() {
    if (!curriculum) return;
    let lastIndex = displayTexts.length - 1;
    if (finalTexts[lastIndex].length > displayTexts[lastIndex].length) {
      displayTexts[lastIndex] = finalTexts[lastIndex].slice(0, displayTexts[lastIndex].length + 1);
      doneWriting = false;
      if (displayTexts[displayTexts[lastIndex].length - 1]) {
        setTimeout(showText, 20); // longer pause between words
      } else {
        setTimeout(showText, 5);
      }
    } else {
      writer = null;
      doneWriting = true;
    }
  }

  afterUpdate(() => {
    if (!writer) {
      writer = setTimeout(showText, 100);
    }
  })

  onMount(() => {
    if (!writer) {
      writer = setTimeout(showText, 500);
    }
  })
</script>

{#key curriculum}
  <div
    class="topic-block-wrapper"
    class:dark={theme == "dark"} 
    in:fade = {{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }}
    out:fade = {{ duration: BLOCK_FADE_OUT_DURATION }} 
  >
    <div
      class="glass-container topic-block"
      bind:this={topicBlock}
    >
      {#if curriculum}
        <h2 class="title">{curriculum.curriculumName}</h2>
        <!-- <div>
          <input bind:value={text}>
        </div> -->
        
        {#each displayTexts as displayText, i}
          {#if i % 2 == 0}
            {#if doneWriting}
              {#key displayText}
              <LatexInterpreter {sendQuery} text={displayText}></LatexInterpreter>
              {/key}
            {:else}
              <p>{@html displayText}</p>
            {/if}
          {:else if !displayText.includes(QUIZ_PROMPT)}
            <p class="color-accent-2">{displayText}</p>
          {:else if displayText.includes(QUIZ_PROMPT)}
            <p class="color-accent-2">{"QUIZ TIME"}</p>
          {/if}
        {/each}
        <button
          class="btn-underline quiz-button"
          on:click={() => sendQuery(QUIZ_PROMPT)}
        >
          Quiz Me
        </button>
      {:else}
        <h2 class="title">{topic.title}</h2>

        <div>
          <h4>Knowledge Requirements</h4>
          <p>{topic.prerequisites["Knowledge Requirements"]}</p>
          <h4>Suggested Preparatory Material</h4>
          <p>{topic.prerequisites["Suggested Preparatory Material"]}</p>
        </div>
        
        <div>
          <h4>Curriculum</h4>
          {#each Object.entries(topic.curriculum) as [curriculumId, curriculumName]}
          <span
            class="btn-transparent"
            on:click={() => changeTopic(curriculumId, curriculumName)}
          >
            {curriculumId} {curriculumName}
          </span>
          <br>
          {/each}
        </div>
      {/if}
    </div>

    {#if curriculum}
      <div class="text-bar">
        <input type="text" bind:value={userQueryInput} placeholder="Ask anything about the topic.." />
        <div class="go-btn" on:click={() => {sendQuery(userQueryInput); userQueryInput = ""}}>{">"}</div>
      </div>
    {/if}
    
  </div>
{/key}

<style lang="scss">
  @import "../../styles/root.scss";
  @import "../../styles/topicBlock.scss";
</style>