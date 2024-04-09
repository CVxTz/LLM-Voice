<template>
  <div>
    <button class="record-button" @mousedown="startRecording" @mouseup="stopRecording">Hold to Record</button>
    <audio ref="audioPlayer" @ended="handleAudioEnded"></audio>
    <div v-if="audioBlobSize !== null">Audio Blob Size: {{ audioBlobSize }} bytes</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRecording: false,
      audioChunks: [],
      mediaRecorder: null,
      stream: null,
      audioURL: null, // Added audioURL property
      audioBlobSize: null // Added audioBlobSize property
    };
  },
  mounted() {
    this.requestMicrophonePermission(); // Request microphone permission when the component is mounted
  },
  methods: {
    async requestMicrophonePermission() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (error) {
        console.error('Error accessing microphone:', error);
      }
    },
    async startRecording() {
      try {
        if (!this.stream) {
          await this.requestMicrophonePermission();
        }
        this.audioChunks = []; // Clear previous audio chunks
        this.mediaRecorder = new MediaRecorder(this.stream);
        this.mediaRecorder.addEventListener('dataavailable', event => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        });
        this.mediaRecorder.start();
        this.isRecording = true;
      } catch (error) {
        console.error('Error accessing microphone:', error);
      }
    },
    stopRecording() {
      if (this.isRecording) {
        this.mediaRecorder.addEventListener('stop', () => {
          this.isRecording = false;
          this.playRecordedAudio(); // Call playRecordedAudio() after recording is stopped
        });
        this.mediaRecorder.stop();
      }
    },
    async playRecordedAudio() {
      const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
      this.audioURL = window.URL.createObjectURL(audioBlob); // Update audioURL with new recording
      this.$refs.audioPlayer.src = this.audioURL;
      this.$refs.audioPlayer.play();
    },
    handleAudioEnded() {
      this.$emit('audio_ready', { audioBlob: new Blob(this.audioChunks, { type: 'audio/wav' }) });
      this.audioBlobSize = this.audioChunks.reduce((acc, chunk) => acc + chunk.size, 0);
    }
  }
};
</script>

<style scoped>
.record-button {
  width: 100px; /* Set your desired width */
  height: 100px; /* Set your desired height */
  border-radius: 50%; /* Make it a circle */
  background-color: red; /* Set button background color */
  color: white; /* Set text color */
  border: 2px solid white; /* Set border color and width */
  font-size: 16px; /* Set font size */
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); /* Add a small shadow */
  transition: transform 0.2s, box-shadow 0.2s; /* Add transition effects */
}

.record-button:active {
  transform: translateY(2px); /* Move the button slightly down when pressed */
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3); /* Adjust shadow when pressed */
}

/* Add your styles here if needed */
</style>
