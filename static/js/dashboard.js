function toggleDropdown(dropdownId) {
    var dropdown = document.getElementById(dropdownId);
    dropdown.classList.toggle('hidden');
}
const video = document.getElementById('video');
const audio = document.getElementById('audio');
const overlay = document.getElementById('overlay');
const overlayText = document.getElementById('overlay-text');
var data = {{ data_json | tojson }};
let currentScene = 1;

function play() {
// Autoplay video
video.play().then(() => {
    // Autoplay audio
    audio.play();

    // Display overlay with text
    overlayText.innerHTML = data[currentScene].text;
    overlay.style.display = 'block';
    overlay.style.animation = 'fade-in 2s forwards';

    // Set up event listener for audio end to trigger the next scene
    audio.addEventListener('ended', next);
}).catch((error) => {
    console.error('Autoplay failed:', error);
});
}

function pause() {
video.pause();
audio.pause();
}

function next() {
// Reset overlay animation
overlay.style.animation = 'none';
void overlay.offsetWidth; // Trigger reflow
overlay.style.animation = null;

// Hide overlay
overlay.style.display = 'none';

// Increment scene
currentScene++;
if (currentScene > {{scene_length-1}}) {
    // Reset to the first scene if reached the end
    currentScene = 1;
}

// Update video, audio, and overlay text
video.src = data[currentScene].video;
audio.src = data[currentScene].audio;
overlayText.innerHTML = data[currentScene].text;

// Play video and audio
play();
}