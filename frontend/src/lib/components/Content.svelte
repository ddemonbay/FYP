<script>
  import { slide, fly, fade } from 'svelte/transition';
  import { afterUpdate, onMount } from 'svelte';
  import TopicBlock from "./TopicBlock.svelte";
  import { GET_STARTED_FADE_IN_DURATION } from '../constants';

  export let block;
  export let theme;

  export let backStack;
  export let forwardStack;

  const LOGIN_FLY_DURATION = 700;
  const BLOCK_FADE_OUT_DURATION = 200;
  const BLOCK_FADE_IN_DELAY = 500;
  const BLOCK_FADE_IN_DURATION = 700;

  let displayText = "";
  let finalText = "";
  let prevBlock = block

  let topics = [
    {
    "title": "Wave",
    "explanation": "wave is related to duality of light, which is a photon exhibits the phenomenon of a particle and a wave.",
    "subTopics": [
      {
        "category": "Prerequesite",
        "courses": [
          {
            "courseId": "0.1",
            "courseName": "linear algebra",
            "explanation": "linear algebra is EZ",
          },
          {
            "courseId": "0.2",
            "courseName": "fundamental quantum physics",
            "explanation": "fundamental quantum physics is not fundamental",
          }
        ]
      }, 
      {
        "category": "Particle Duality",
        "courses": [
          {
            "courseId": "1.1",
            "courseName": "photon",
            "explanation": "photon is light",
          },
          {
            "courseId": "1.2",
            "courseName": "particle property",
            "explanation": "it is like atom",
          }
        ]
      }
    ]
  },
  {
    "title": "linear algebra",
    "explanation": "wave is related to duality of light, which is a photon exhibits the phenomenon of a particle and a wave.",
    "subTopics": [
      {
        "category": "Metrix",
        "courses": [
          {
            "courseId": "1.1",
            "courseName": "vector space",
            "explanation": "vector space (also called a linear space) is a set whose elem...",
          },
          {
            "courseId": "1.2",
            "courseName": "linear maps",
            "explanation": "Linear maps are mappings between vector spaces that pres...",
          }
        ]
      }
    ]
  }
  ]
  let topic = topics[0];

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

  const selectTopicBlock = (selectedTopic) => {
    block = "topic-block";
    topic = topics.find((t) => t == selectedTopic);
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
    console.log(backStack, forwardStack)
  }
  
  const back = () => {
    forwardStack.push(block);
    block = backStack.pop();
    console.log(backStack, forwardStack)
  }

  const forward = () => {
    backStack.push(block);
    block = forwardStack.pop();
    console.log(backStack, forwardStack)
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

  {#if block != "login" && forwardStack.length != 0 }
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
      <button class="btn-underline" on:click={() => {block = "loading"; setTimeout(() => {block = "action"}, LOGIN_FLY_DURATION)}} style="left: 1px">Submit</button>
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
        <input type="text" placeholder="Search a topic you want to learn.." />
        <div class="go-btn" on:click={() => navToBlock("topic-block")}>{">"}</div>
      </div>
    </div>
  {/if}

  {#if block == "resume-topic"}
    <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <p>{displayText}</p>
      <ul>
        {#each topics as topic}
          <li
            on:click={() => selectTopicBlock(topic)}
            class="btn-transparent"
          >
            {topic.title}
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  {#if block == "topic-block"}
    <div class="block" in:fade={{ delay: BLOCK_FADE_IN_DELAY, duration: BLOCK_FADE_IN_DURATION }} out:fade={{ duration: BLOCK_FADE_OUT_DURATION }}>
      <TopicBlock bind:topic bind:topics bind:theme />
    </div>
  {/if}

</div>

<style lang="scss">
  @import "../../root.scss";

  .content-container {
    width: 100%;
    height: 100%;
    text-align: left;
    display: flex;
    justify-content: center;
    // position: relative;
  }
  
  .block {
    font-size: 1.16em;
    width: 80%;
    position: absolute;
    top: $content-margin-top;

    & > *+* {
      margin-bottom: 1em;
    }
  }

  .login-block {
    font-family: "barlow condensed";
    text-align: center;
    margin: auto;
    width: 30em;
    padding: .8em 1.4em;
    
    h2 {
      margin-top: 0;
      font-size: 2.8em;
    }
    
    p {
      margin-bottom: 1.5em;
    }

    input, button {
      margin-top: 2.6em;
    }
  }

  .action-block {
    width: 38%;
    text-align: center;
  }

  .card {
    padding: 1em;
    cursor: pointer;
    transition: .4s;
  
    &:hover {
      background: rgba( 255, 255, 255, 0.13 );
      color: rgba( 255, 255, 255, 0.74 );
    }
  }

  .choice-container {
    display: flex;
    justify-content: center;

    & > * + * {
      margin-left: 1em;
    }
  }

  .back-button {
    position: absolute;
    top: 50%;
    left: 8%;
    font-size: 1.4rem;
    cursor: pointer;
  }

  .forward-button {
    position: absolute;
    top: 50%;
    right: 8%;
    font-size: 1.4rem;
    cursor: pointer;
  }
</style>