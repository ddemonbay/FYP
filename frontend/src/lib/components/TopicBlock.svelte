<script>
  import { afterUpdate, onMount } from "svelte";
  import { fade, fly } from "svelte/transition";

  export let topics;
  export let topic;
  export let theme;

  let displayText = "";
  let writer;

  let subTopic = topics[1];
  let finalText = topic.explanation;

  const changeTopic = () => {
    topic = subTopic;
  }

  onMount(() => {
    if (!writer) {
      writer = setTimeout(showText, 500);
    }
  })

  function showText() {
    if (finalText.length > displayText.length) {
      displayText = finalText.slice(0, displayText.length + 1);

      if (displayText[displayText.length - 1]) {
        setTimeout(showText, 20); // longer pause between words
      } else {
        setTimeout(showText, 5);
      }
    } else {
      writer = null
    }
  }

  afterUpdate(() => {
    if (!writer) {
      writer = setTimeout(showText, 100);
    }
  })
</script>

{#key topic}
  <div
    class="topic-block-wrapper"
    in:fade = {{ delay: 170, duration: 600 }}
    out:fade = {{ duration: 200 }}
  >
    <div
      class="glass-container topic-block"
      class:dark={theme == "dark"} 
    >
      <h2 class="title">{topic.title}</h2>
      
    
      <div class="sub-courses-block">
        {#each topic.subTopics as subTopic}
        <div>
          <h4>{subTopic.category}</h4>
          {#each subTopic.courses as course}
          <span
           class="btn-transparent"
           on:click={changeTopic}
          >
            {course.courseId} {course.courseName}
          </span>
          <br>
          {/each}
        </div>
        {/each}
      </div>
      <button class="btn-underline quiz-button">Quiz Me</button>
      <p>{@html displayText.replace(/\n/g, '<br>')}</p>
    </div>

    <div class="text-bar">
      <input type="text" placeholder="Ask anything about the topic.." />
      <div class="go-btn" on:click={() => (finalText += "<br>ssjdsiojfsjj sjdfjs sdjf oijs ojf oisjdo o os fs.")}>{">"}</div>
    </div>
  </div>
{/key}

<style lang="scss">
  @import "../../root.scss";

  .text-bar {
    margin-top: 1.2em;
  }

  .text-bar input {
    width: 80%;
  }

  .glass-container {
    padding: 1em 1.2em;
  }

  .title { 
    color: rgb(42, 0, 126);
  }

  .topic-block-wrapper {
    position: absolute;
    width: 100%;
  }

  .topic-block {
    max-height: 60vh;
    overflow: auto;

    &::-webkit-scrollbar {
      width: 8px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }
    
    &::-webkit-scrollbar-thumb {
      background: rgba(42, 0, 126,.6); // rgba(255,255,255,0.3)
      border-radius: 10px;
      
      &:hover {
        background: rgba(42, 0, 126,.8); 
      }
    }

    ::-webkit-scrollbar-thumb:hover {
      background: rgba(42, 0, 126,.9); 
      scrollbar-color: rgba(42, 0, 126,1) rgba(255,255,255,0);
    }

    .btn-transparent {
      font-style: italic;
    }

    h2 {
      margin-top: .2em;
    }
    h4 {
      margin-bottom: .6em;
    }

    .btn-underline {
      margin-top: 1em;
    }
  }

  .sub-courses-block {
    // background: rgba(#fff, .4);
  }
  
  // temp approach
  .dark {
    background: rgba( #000, 0.23 );
    box-shadow: 0 8px 32px 0 rgba(#000, 0.15);

    input[type="text"], input[type="password"] { // reduce the stacking color
      background: rgba(#000, .08);
    }
  }
</style>