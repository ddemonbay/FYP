<script>
  import { slide, fly, fade } from 'svelte/transition';
  import { afterUpdate, onMount } from 'svelte';
  import TopicBlock from "./TopicBlock.svelte";
  import { GET_STARTED_FADE_IN_DURATION } from '../constants';

  export let block;
  export let theme;

  export let backStack;
  export let forwardStack;
  export let curriculum;
  export let curriculumHist;

  const LOGIN_FLY_DURATION = 700;
  const BLOCK_FADE_OUT_DURATION = 200;
  const BLOCK_FADE_IN_DELAY = 500;
  const BLOCK_FADE_IN_DURATION = 700;
  const BACKEND_URL = "https://ugymjg1tfk.execute-api.us-east-1.amazonaws.com/Implementation/tutorial";

  let displayText = "";
  let finalText = "";
  let prevBlock = block
  let topicInput = "";
  let username = "damon";
  let topicIdPair;
  let finalTexts = [];
  let displayTexts = [];

  let topic;

  function showText() {
    if (finalText.length > displayText.length) {
      displayText = finalText.slice(0, displayText.length + 1);

      if (displayText[displayText.length - 1]) {
        setTimeout(showText, 20); // longer pause between words
      } else {
        setTimeout(showText, 5);
      }
    } else {
      // showButton
    }
  }

  async function selectTopicBlock(selectedTopicId) {
    navToBlock("loading");
    topic = await getTopic(selectedTopicId);
    curriculum = null;
    curriculumHist = null;
    block = "topic-block";
  }

  async function getTopic(topicId) {
    let getPrerequisitesResponse = await fetch(BACKEND_URL + "/getPrerequisites", {
      method: "POST",
      body: JSON.stringify({
        topicId: topicId,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let getPrerequisitesData = await getPrerequisitesResponse.json();
    if (getPrerequisitesData == "Error") {
      getPrerequisitesData = {"prerequisites": {
			"Knowledge Requirements": "",
			"Suggested Preparatory Material": "",
		}}
    }
    

    let getCurriculumResponse = await fetch(BACKEND_URL + "/getCurriculum", {
      method: "POST",
      body: JSON.stringify({
        topicId: topicId,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let getCurriculumData = await getCurriculumResponse.json();
    if (getCurriculumData == "Error") {
      getCurriculumData = {"curriculum": {}}
    }

    return {
      "topicId": topicId,
      "title": topicIdPair[topicId],
      "prerequisites": getPrerequisitesData["prerequisites"],
      "curriculum": getCurriculumData["curriculum"],
    }
  }

  // preserve nav hist
  const navToBlock = (name) => {
    backStack.push(block);
    if (name != forwardStack[forwardStack.length - 1]) { // if new action != forward action
      forwardStack = [];
    } else { // same action == forward -> pop forward stack
      forwardStack.pop();
    }
    block = name;
  }
  
  const back = () => {
    if (block == "topic-block" && curriculum != null) {
      curriculumHist = curriculum;
      curriculum = null;
    } else {
      forwardStack.push(block);
      block = backStack.pop();
    }
  }

  const forward = () => {
    if (block == "topic-block" && curriculumHist != null) {
      curriculum = curriculumHist;
      curriculumHist = null;
    } else {
      backStack.push(block);
      block = forwardStack.pop();
    }
  }

  async function searchTopic() {
    navToBlock("loading");

    let topicId;
    let generateTopicResponse = await fetch(BACKEND_URL + "/generateTopic", {
      method: "POST",
      body: JSON.stringify({
        topic: topicInput,
      }),
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let generateTopicData = await generateTopicResponse.json();

    if (generateTopicData == "Topic Exist") {
      for (let i in topicIdPair) {
        if (topicIdPair[i].toLowerCase().trim() == topicInput.toLowerCase().trim()) {
          topicId = i;
        }
      }
    } else if (generateTopicData.includes("Topic ID:")) {
      topicId = parseInt(generateTopicData.substring(9));
    } else {
      console.log("error occuring connecting to backend");
      block = "topic-search";
    }
    topic = await getTopic(topicId)
    
    topicIdPair = await getTopicIdPair();
    block = "topic-block";
    topicInput = "";
  }

  async function login() {
    block = "loading";
    topicIdPair = await getTopicIdPair();
    
    setTimeout(() => {
      block = "action"
    }, LOGIN_FLY_DURATION)
  }

  async function getTopicIdPair() {
    let getTopicIdPairResponse = await fetch(BACKEND_URL + "/getTopicIdPair", {
      method: "POST",
      headers: {
        "authorizationUserLoginToken": "qwertyuiop:" + username,
      }
    });

    let getTopicIdPairData = await getTopicIdPairResponse.json();
    return getTopicIdPairData["topicIdPair"];
  }

  afterUpdate(() => {
    if (block != prevBlock) {
      displayText = "";

      if (block == "action") {
        finalText = "Get started"
      } else if (block == "topic-search") {
        finalText = "Search for a topic you want to learn...";
      } else if (block == "resume-topic") {
        finalText = "Pick a topic to resume...";
      }
      prevBlock = block;
      setTimeout(showText, 500);
    }
  })
</script>

<div class="content-container" class:dark={theme=="dark"}>
  {#if block != "login" && backStack.length != 0 }
    <div
      class="back-button"
      on:click={() => back()}
    >
      {"<"}
    </div>
  {/if}

  {#if block != "login" && (forwardStack.length != 0 || (block == "topic-block" && curriculumHist != null)) }
    <div
      class="forward-button"
      on:click={() => forward()}
    >
      {">"}
    </div>
  {/if}

  {#if block == "login"}
    <div class="login-block glass-container" in:fly={{ y: -70, duration: 800 }} out:fly={{ y: -90, duration: LOGIN_FLY_DURATION }}>
      <h2 class="logo">AI Tutor</h2>
      <p>Please login to start your learning journey</p>
      <input type="text" placeholder="Username"/>
      <input type="password" placeholder="Password"/>
      <button class="btn-underline" on:click={() => login()} style="left: 1px">Submit</button>
    </div>
  {/if}
  
  {#if block == "action"}
    <div class="block action-block" in:fade={{ duration: GET_STARTED_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <h3 class="condensed">Get started</h3>
      <div class="choice-container">
        <div class="glass-container card" on:click={() => navToBlock("topic-search")}>New Topic</div>
        <div class="glass-container card" on:click={() => navToBlock("resume-topic")}>Resume Topic</div>
      </div>
    </div>
  {/if}

  {#if block == "topic-search"}
    <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <p>{displayText}</p>
      <div class="text-bar">
        <input type="text" bind:value={topicInput} placeholder="Search a topic you want to learn.." />
        <div class="go-btn" on:click={() => searchTopic()}>{">"}</div>
      </div>
    </div>
  {/if}

  {#if block == "resume-topic"}
    <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <p>{displayText}</p>
      <ul>
        {#each Object.entries(topicIdPair) as [topicId, title]}
          <li
            on:click={() => selectTopicBlock(topicId)}
            class="btn-transparent"
          >
            {title}
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  {#if block == "topic-block"}
    <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <TopicBlock bind:topic bind:curriculum bind:theme bind:block bind:finalTexts bind:displayTexts />
    </div>
  {/if}

  {#if block == "loading"}
  <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
    <div class="loading-screen">
      <p>.............</p>
    </div>
  </div>
  {/if}

</div>

<style lang="scss">
  @import "../../styles/root.scss";
  @import "../../styles/content.scss";    
</style>