const query = (obj) =>
  Object.keys(obj)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
    .join("&"); 

let baseaudio; 
let baseaudio1;
let base64Image;
const greeting = document.getElementById("greeting");
const image_upload = document.getElementById("imgUploadInput");
const audio_icon = document.getElementById("audioIcon");
const colorThemes = document.querySelectorAll('[name="theme"]');
const markdown = window.markdownit();
const message_box = document.getElementById(`messages`);
const message_input = document.getElementById(`message-input`);
const box_conversations = document.querySelector(`.top`);
const spinner = box_conversations.querySelector(".spinner");
const stop_generating = document.querySelector(`.stop_generating`);
const send_button = document.querySelector(`#send-button`);
const mic_button = document.querySelector(`#mic-button`);
const image_button = document.querySelector(`#image-button`);
let prompt_lock = false;

hljs.addPlugin(new CopyButtonPlugin());

// sidebar TOGGLE FUNCTIONALITY
const desktopSidebarToggle = document.querySelector(".desktop-sidebar-toggle");
const sidebar = document.querySelector(".conversations");

desktopSidebarToggle.addEventListener("click", (event) => {
  sidebar.classList.toggle("shown");
  sidebar.classList.toggle("hidden");
  event.target.classList.toggle("rotated");
  window.scrollTo(0, 0);
});

function openFilePicker() {
  const fileInput = document.getElementById("image-upload");
  fileInput.click();
}

const fileInput = document.getElementById("image-upload");
fileInput.addEventListener("change", handleImageUpload);

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (file && file.type.startsWith("image/")) {
    // Handle the uploaded image here
    const reader = new FileReader();
    reader.onload = function () {
      // The reader.result contains the base64-encoded image data
      const imageData = reader.result;
      // Do something with the imageData, e.g., send it to the server or display it
      console.log(imageData);
    };
    reader.readAsDataURL(file);
  } else {
    // Handle the case where the selected file is not an image
    console.error("Please select an image file.");
  }
}

//	AUDIO INPUT FUNCTIONALITY
let isRecording = false;
let mediaRecorder = null;

audio_icon.addEventListener("click", () => {
  if (!isRecording) {
    startRecording();
    isRecording = true;
    audio_icon.classList.add("recording");
  } else {
    stopRecording();
    isRecording = false;
    audio_icon.classList.remove("recording");
  }
});

function startRecording() {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaRecorder = new MediaRecorder(stream);
      let chunks = [];

      mediaRecorder.ondataavailable = (event) => {
        chunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "audio/webm" });
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = () => {
          baseaudio = reader.result.split(",")[1];
        };
        chunks = [];
      };

      console.log(baseaudio);
      mediaRecorder.start();
    })
    .catch((err) => {
      console.error("Error accessing audio stream: ", err);
    });
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

function handleImageUpload(event) {

  const file = event.target.files[0];

  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = function () {
      base64Image = convertToBase64(reader.result);
      console.log(base64Image);
    };
    reader.readAsDataURL(file);
  } else {
    console.error("Please select an image file.");
  }
}

function convertToBase64(imageData) {
  // Split the base64 string into two parts
  const parts = imageData.split(",");

  // Check if the string is a valid base64 string with a data URI scheme
  if (parts.length !== 2 || !parts[0].includes("data:image/")) {
    throw new Error("Invalid image data");
  }

  // Return the base64 part of the string
  return parts[1];
}

function resizeTextarea(textarea) {
  textarea.style.height = "80px";
  textarea.style.height = Math.min(textarea.scrollHeight, 200) + "px";
}

const format = (text) => {
  return text.replace(/(?:\r\n|\r|\n)/g, "<br>");
};

message_input.addEventListener("blur", () => {
  window.scrollTo(0, 0);
});

const delete_conversations = async () => {
  localStorage.clear();
  await new_conversation();
};

const handle_ask = async () => {
  message_input.style.height = `80px`;
  message_input.focus();

  window.scrollTo(0, 0);
  let message = message_input.value;

  if (message.length > 0) {
    message_input.value = ``;
    await ask_gpt(message);
  }
};

const remove_cancel_button = async () => {
  stop_generating.classList.add(`stop_generating-hiding`);

  setTimeout(() => {
    stop_generating.classList.remove(`stop_generating-hiding`);
    stop_generating.classList.add(`stop_generating-hidden`);
  }, 300);
};

const clear_conversations = async () => {
  const elements = box_conversations.childNodes;
  let index = elements.length;

  if (index > 0) {
    while (index--) {
      const element = elements[index];
      if (
        element.nodeType === Node.ELEMENT_NODE &&
        element.tagName.toLowerCase() !== `button`
      ) {
        box_conversations.removeChild(element);
      }
    }
  }
};

const clear_conversation = async () => {
  let messages = message_box.getElementsByTagName(`div`);

  while (messages.length > 0) {
    message_box.removeChild(messages[0]);
  }
};

const show_option = async (conversation_id) => {
  const conv = document.getElementById(`conv-${conversation_id}`);
  const yes = document.getElementById(`yes-${conversation_id}`);
  const not = document.getElementById(`not-${conversation_id}`);

  conv.style.display = "none";
  yes.style.display = "block";
  not.style.display = "block";
};

const hide_option = async (conversation_id) => {
  const conv = document.getElementById(`conv-${conversation_id}`);
  const yes = document.getElementById(`yes-${conversation_id}`);
  const not = document.getElementById(`not-${conversation_id}`);

  conv.style.display = "block";
  yes.style.display = "none";
  not.style.display = "none";
};

const delete_conversation = async (conversation_id) => {
  localStorage.removeItem(`conversation:${conversation_id}`);

  const conversation = document.getElementById(`convo-${conversation_id}`);
  conversation.remove();

  if (window.conversation_id == conversation_id) {
    await new_conversation();
  }

  await load_conversations(20, 0, true);
};

const set_conversation = async (conversation_id) => {
  history.pushState({}, null, `/chat/${conversation_id}`);
  window.conversation_id = conversation_id;

  await clear_conversation();
  await load_conversation(conversation_id);
  await load_conversations(20, 0, true);
};

function hideGreeting() {
  greeting.classList.remove("show-greeting");
  greeting.classList.add("hide-greeting");
}

const new_conversation = async () => {
  console.log("new_convn() loaded");
  history.pushState({}, null, `/chat/`);
  window.conversation_id = uuid();

  await clear_conversation();
  await load_conversations(20, 0, true);

  // SHOWS GREETING ON NEW CONVO
  console.log(greeting.classList);
  greeting.classList.remove("hide-greeting");
  greeting.classList.add("show-greeting");
  console.log(greeting.classList);

  hideGreeting(); // Call the hideGreeting function here
};

const ask_gpt = async (message, image_base64 = null) => {
  try {
    message_input.value = ``;
    message_input.innerHTML = ``;
    message_input.innerText = ``;

    add_conversation(window.conversation_id, message.substr(0, 20));
    window.scrollTo(0, 0);
    window.controller = new AbortController();

    prompt_lock = true;
    window.text = ``;
    window.token = message_id();

    stop_generating.classList.remove(`stop_generating-hidden`);

    // HIDES GREETING MESSAGE ON CONVO START
    greeting.classList.remove("show-greeting");
    greeting.classList.add("hide-greeting");

    message_box.innerHTML += `
            <div class="message">
                <div class="user">
                    ${user_image}
                </div>
                <div class="content" id="user_${token}"> 
                    <b>${format(message)}</b>
                </div>
            </div>
        `;

    /* .replace(/(?:\r\n|\r|\n)/g, '<br>') */

    message_box.scrollTop = message_box.scrollHeight;
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 500));
    window.scrollTo(0, 0);

    message_box.innerHTML += `
            <div class="message">
                <div class="user">
                    ${gpt_image} 
                </div>
                <div class="content" id="gpt_${window.token}">
                    <div id="cursor"></div>
                </div>
            </div>
        `;

    message_box.scrollTop = message_box.scrollHeight;
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 1000));
    window.scrollTo(0, 0);

    const response = await fetch(`/backend-api/v2/conversation`, {
      method: `POST`,
      headers: {
        "content-type": `application/json`,
      },
      body: JSON.stringify({
        message,
        is_image: image_base64 !== null,
        image_base64,
        language: document.getElementById("language").value,
        output: document.getElementById("mode").value,
        base64Audio: baseaudio,
        base64Image: base64Image,
      }),
    });

    ///

    const data = await response.json();

    if (data.success) {
      const responseContainer = document.getElementById(`gpt_${window.token}`);
      responseContainer.innerHTML = ""; // Clear the previous response

      if (data.response.includes("cloudflarestorage")) {
        // It's an image
        const img = document.createElement("img");
        img.src = data.response;
        img.alt = "Response Image";
        img.className = "response-image";
        img.onerror = () => {
          img.alt = "Image failed to load";
        };
        responseContainer.appendChild(img);
      } else {
        // It's a text response
        text = data.response;
        responseContainer.innerHTML = markdown.render(text);
        document.querySelectorAll(`code`).forEach((el) => {
          hljs.highlightElement(el);
        });
      }

      add_message(window.conversation_id, "user", message);
      add_message(window.conversation_id, "assistant", data.response);
    } else {
      let error_message = `oops ! something went wrong, please try again / reload. [stacktrace in console]`;
      document.getElementById(`gpt_${window.token}`).innerHTML = error_message;
      add_message(window.conversation_id, "assistant", error_message);
      console.error(data.error);
    }

    ///

    message_box.scrollTop = message_box.scrollHeight;
    await remove_cancel_button();
    prompt_lock = false;

    await load_conversations(20, 0);
    window.scrollTo(0, 0);
  } catch (e) {
    add_message(window.conversation_id, "user", message);

    message_box.scrollTop = message_box.scrollHeight;
    await remove_cancel_button();
    prompt_lock = false;

    await load_conversations(20, 0);

    console.log(e);

    let cursorDiv = document.getElementById(`cursor`);
    if (cursorDiv) cursorDiv.parentNode.removeChild(cursorDiv);

    if (e.name != `AbortError`) {
      let error_message = `oops ! something went wrong, please try again / reload. [stacktrace in console]`;

      document.getElementById(`gpt_${window.token}`).innerHTML = error_message;
      add_message(window.conversation_id, "assistant", error_message);
    } else {
      document.getElementById(`gpt_${window.token}`).innerHTML += ` [aborted]`;
      add_message(window.conversation_id, "assistant", text + ` [aborted]`);
    }

    window.scrollTo(0, 0);
  }
};

function hideGreeting() {
  greeting.classList.remove("show-greeting");
  greeting.classList.add("hide-greeting");
}

const load_conversation = async (conversation_id) => {
  console.log("load_convn() loaded");
  hideGreeting(); // Call hideGreeting function here

  let conversation = await JSON.parse(
    localStorage.getItem(`conversation:${conversation_id}`)
  );
  console.log(conversation, conversation_id);

  for (item of conversation.items) {
    message_box.innerHTML += `
            <div class="message">
                <div class="user">
                    ${item.role == "assistant" ? gpt_image : user_image}
                </div>
                <div class="content">
                    ${
                      item.role == "assistant"
                        ? markdown.render(item.content)
                        : item.content
                    }
                </div>
            </div>
        `;
  }

  document.querySelectorAll(`code`).forEach((el) => {
    hljs.highlightElement(el);
  });

  message_box.scrollTo({ top: message_box.scrollHeight, behavior: "smooth" });

  setTimeout(() => {
    message_box.scrollTop = message_box.scrollHeight;
  }, 500);
};

const get_conversation = async (conversation_id) => {
  let conversation = await JSON.parse(
    localStorage.getItem(`conversation:${conversation_id}`)
  );
  return conversation.items;
};

const add_conversation = async (conversation_id, title) => {
  if (localStorage.getItem(`conversation:${conversation_id}`) == null) {
    localStorage.setItem(
      `conversation:${conversation_id}`,
      JSON.stringify({
        id: conversation_id,
        title: title,
        items: [],
      })
    );
  }
};

const add_message = async (conversation_id, role, content) => {
  before_adding = JSON.parse(
    localStorage.getItem(`conversation:${conversation_id}`)
  );

  before_adding.items.push({
    role: role,
    content: content,
  });

  localStorage.setItem(
    `conversation:${conversation_id}`,
    JSON.stringify(before_adding)
  ); // update conversation
};

const load_conversations = async (limit, offset, loader) => {
  //console.log(loader);
  //if (loader === undefined) box_conversations.appendChild(spinner);

  let conversations = [];
  for (let i = 0; i < localStorage.length; i++) {
    if (localStorage.key(i).startsWith("conversation:")) {
      let conversation = localStorage.getItem(localStorage.key(i));
      conversations.push(JSON.parse(conversation));
    }
  }

  //if (loader === undefined) spinner.parentNode.removeChild(spinner)
  await clear_conversations();

  for (conversation of conversations) {
    box_conversations.innerHTML += `
    <div class="convo" id="convo-${conversation.id}">
      <div class="left" onclick="set_conversation('${conversation.id}')">
          <i class="fa-regular fa-comments"></i>
          <span class="convo-title">${conversation.title}</span>
      </div>
      <i onclick="show_option('${conversation.id}')" class="fa-regular fa-trash" id="conv-${conversation.id}"></i>
      <i onclick="delete_conversation('${conversation.id}')" class="fa-regular fa-check" id="yes-${conversation.id}" style="display:none;"></i>
      <i onclick="hide_option('${conversation.id}')" class="fa-regular fa-x" id="not-${conversation.id}" style="display:none;"></i>
    </div>
    `;
  }

  document.querySelectorAll(`code`).forEach((el) => {
    hljs.highlightElement(el);
  });
};

document.getElementById(`cancelButton`).addEventListener(`click`, async () => {
  window.controller.abort();
  console.log(`aborted ${window.conversation_id}`);
});

function h2a(str1) {
  var hex = str1.toString();
  var str = "";

  for (var n = 0; n < hex.length; n += 2) {
    str += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
  }

  return str;
}

const uuid = () => {
  return `xxxxxxxx-xxxx-4xxx-yxxx-${Date.now().toString(16)}`.replace(
    /[xy]/g,
    function (c) {
      var r = (Math.random() * 16) | 0,
        v = c == "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    }
  );
};

const message_id = () => {
  random_bytes = (Math.floor(Math.random() * 1338377565) + 2956589730).toString(
    2
  );
  unix = Math.floor(Date.now() / 1000).toString(2);

  return BigInt(`0b${unix}${random_bytes}`).toString();
};

window.onload = async () => {
  load_settings_localstorage();

  conversations = 0;
  for (let i = 0; i < localStorage.length; i++) {
    if (localStorage.key(i).startsWith("conversation:")) {
      conversations += 1;
    }
  }

  if (conversations == 0) localStorage.clear();

  await setTimeout(() => {
    load_conversations(20, 0);
  }, 1);

  if (!window.location.href.endsWith(`#`)) {
    if (/\/chat\/.+/.test(window.location.href)) {
      await load_conversation(window.conversation_id);
    }
  }

  message_input.addEventListener(`keydown`, async (evt) => {
    if (prompt_lock) return;
    if (evt.keyCode === 13 && !evt.shiftKey) {
      evt.preventDefault();
      console.log("pressed enter");
      await handle_ask();
    } else {
      message_input.style.removeProperty("height");
      message_input.style.height = message_input.scrollHeight + 4 + "px";
    }
  });

  send_button.addEventListener(`click`, async () => {
    console.log("clicked send");
    if (prompt_lock) return;
    await handle_ask();
  });

  register_settings_localstorage();
};

document.querySelector(".mobile-sidebar").addEventListener("click", (event) => {
  const sidebar = document.querySelector(".conversations");

  if (sidebar.classList.contains("shown")) {
    sidebar.classList.remove("shown");
    event.target.classList.remove("rotated");
  } else {
    sidebar.classList.add("shown");
    event.target.classList.add("rotated");
  }

  window.scrollTo(0, 0);
});

const register_settings_localstorage = async () => {
  settings_ids = ["switch", "model", "jailbreak"];
  settings_elements = settings_ids.map((id) => document.getElementById(id));
  settings_elements.map((element) =>
    element.addEventListener(`change`, async (event) => {
      switch (event.target.type) {
        case "checkbox":
          localStorage.setItem(event.target.id, event.target.checked);
          break;
        case "select-one":
          localStorage.setItem(event.target.id, event.target.selectedIndex);
          break;
        default:
          console.warn("Unresolved element type");
      }
    })
  );
};

const load_settings_localstorage = async () => {
  settings_ids = ["switch", "model", "jailbreak"];
  settings_elements = settings_ids.map((id) => document.getElementById(id));
  settings_elements.map((element) => {
    if (localStorage.getItem(element.id)) {
      switch (element.type) {
        case "checkbox":
          element.checked = localStorage.getItem(element.id) === "true";
          break;
        case "select-one":
          element.selectedIndex = parseInt(localStorage.getItem(element.id));
          break;
        default:
          console.warn("Unresolved element type");
      }
    }
  });
};

// Theme storage for recurring viewers
const storeTheme = function (theme) {
  localStorage.setItem("theme", theme);
};

// set theme when visitor returns
const setTheme = function () {
  const activeTheme = localStorage.getItem("theme");
  colorThemes.forEach((themeOption) => {
    if (themeOption.id === activeTheme) {
      themeOption.checked = true;
    }
  });
  // fallback for no :has() support
  document.documentElement.className = activeTheme;
};

colorThemes.forEach((themeOption) => {
  themeOption.addEventListener("click", () => {
    storeTheme(themeOption.id);
    // fallback for no :has() support
    document.documentElement.className = themeOption.id;
  });
});

document.onload = setTheme();
